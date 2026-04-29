import json
import pickle
import sys
from collections import Counter
from datetime import datetime, timedelta
from itertools import groupby
from pathlib import Path
from typing import Dict, List

from em.em_tree import AnyTreeNode, type_to_children_property_map
from ..metrics.categories import FineEmvOutputCategory, BroadEmvOutputCategory

sys.path.append(str((Path(__file__).parent.parent.parent.parent / 'experiments' / 'demo').resolve()))
from experiments.demo.create_incremental_tree_demo import load_incremental_tree_steps_from_logfile, TreeNode


def _tree_size(t: TreeNode):
    # noinspection PyTypeChecker
    return 1 + sum(_tree_size(c)
                   for c in t.children
                   if c != 'hidden')


def _find_leafs_in_range(n: AnyTreeNode, start: datetime, end: datetime):
    n_start, n_end = n.range if hasattr(n, 'range') else (n.raw.timestamp, n.raw.timestamp)
    if type(n) not in type_to_children_property_map:
        return [n] if start <= n_start <= n_end <= end else []
    children = getattr(n, type_to_children_property_map[type(n)])
    result = []
    for c in children:
        result += _find_leafs_in_range(c, start, end)
    return result


def _eval_relevant_forgotten_ratio(exp_dir: Path, full_results: List[Dict], history_ids: List[str]):
    if not all('ref_ts' in r for r in full_results):
        return {1: 0, 2: 0}

    # Relevant information that was forgotten
    #  Use the history pickle files for this instead of tree state log
    forgotten_count_per_round = {1: 0, 2: 0}
    total_count_per_round = dict(forgotten_count_per_round)
    for history_id in history_ids:
        relevant_samples = [r for r in full_results
                            if r['id'].split('-')[:history_id.count('-') + 1] == history_id.split('-')]
        # Unfortunately, r['q_time'] does not necessarily correspond to the history file name due to clamping
        #  to the nearest scene before => need to get all history files and take the closest before.
        all_histories = [
            pickle.loads(history_file.read_bytes())
            for history_file in (exp_dir / history_id).glob('*.history.pkl')
        ]
        all_histories.sort(key=lambda h: h.range)
        for r in relevant_samples:
            sample_time = datetime.strptime(r['q_time'], '%Y/%m/%d %H:%M:%S').replace(microsecond=999999)
            histories_before = [h for h in all_histories
                                if h.range[1] < sample_time]
            assert len(histories_before) >= 1
            history = histories_before[-1]
            assert (sample_time - history.range[-1]).total_seconds() < 60
            # Assume only one ref_ts for now
            start, end = (datetime.strptime(ts, '%Y/%m/%d %H:%M:%S') for ts in r['ref_ts'][0])
            # Account for rounding / microsecond cutoff
            start = start - timedelta(seconds=1, microseconds=-1)
            end = end + timedelta(seconds=1, microseconds=-1)
            relevant_leafs = _find_leafs_in_range(history, start, end)
            q_pair_idx = r['meta']['q_pair_idx']
            if all(hasattr(x, '_forgotten') for x in relevant_leafs):
                forgotten_count_per_round[q_pair_idx] += 1
            total_count_per_round[q_pair_idx] += 1
    return {
        k: forgotten_count_per_round[k] / total_count_per_round[k]
        for k in forgotten_count_per_round.keys()
    }


def eval_exp_dir(exp_dir: Path):
    assert exp_dir.is_dir()
    results_file = exp_dir / 'results.json'
    assert results_file.is_file()
    auto_eval_file = list(exp_dir.glob('results.*.auto_eval.json'))[0]

    results: dict = json.loads(results_file.read_text())
    eval_results = json.loads(auto_eval_file.read_text())['results']
    history_ids = [d.name for d in exp_dir.iterdir() if d.is_dir() and (d / 'tree-states.log').is_file()]

    num_qa = len(results['results'])
    num_histories = len(history_ids)

    # QA performance
    full_results = [
        {
            'id': q_id,
            'cat': eval_results[q_id]['cat'] if 'cat' in eval_results[q_id] else 'wrong',
            **q_dict,
        }
        for q_id, q_dict in results['results'].items()
    ]
    cat_counter = Counter([
        FineEmvOutputCategory(r['cat']).broad.name
        for r in full_results
    ])
    change_stats = {
        'better': 0, 'same': 0, 'worse': 0
    }
    cat_counter_before, cat_counter_after = Counter(), Counter()
    if all('meta' in s for s in full_results):
        full_results.sort(key=lambda s: s['meta']['q_pair_id'])  # For group_by to work correctly
        pairs = groupby(full_results, key=lambda s: s['meta']['q_pair_id'])
        num_pairs = 0
        for _, pair in pairs:
            pair = list(pair)
            if len(pair) != 2:
                print('Skipping incomplete pair!', pair)
                continue
            num_pairs += 1
            pair.sort(key=lambda p: p['q_time'])
            cat_before, cat_after = [FineEmvOutputCategory(p['cat']).broad for p in pair]
            cat_counter_before[cat_before.name] += 1
            cat_counter_after[cat_after.name] += 1
            if cat_before.index < cat_after.index:
                change_stats['worse'] += 1
            elif cat_before.index == cat_after.index:
                change_stats['same'] += 1
            else:
                change_stats['better'] += 1
    else:
        num_pairs = 1  # To avoid division by zero

    # Token/Time costs
    qa_time = results['times']['qa']
    forgetting_time = results['times']['forgetting']
    qa_prompt_tokens = results['token_costs']['qa']['prompt_tokens']
    forgetting_prompt_tokens = results['token_costs']['forgetting']['prompt_tokens']

    qa_time_per_q = qa_time / num_qa
    qa_tokens_per_q = qa_prompt_tokens / num_qa
    forgetting_time_per_h = forgetting_time / num_histories
    forgetting_tokens_per_h = forgetting_prompt_tokens / num_histories

    cfg = results['config']
    is_offline = (cfg['dataset_type'] == 'teach-full'
                  or cfg['dataset_type'] == 'armarx' and cfg['online_builder_args'] == 'None'
                  or 'ego' in cfg['dataset_type'] and cfg['history_builder_args'] == 'None')
    # Offline => include builder costs in QA costs. But need to use correct denominator: number of QA times
    if is_offline:
        builder_tokens = results['token_costs']['builder']['prompt_tokens']
        builder_time = results['times']['builder']
        num_qa_times = len(set(r['q_time'] for r in full_results))
        print('Offline mode! num_qa_times =', num_qa_times)
        builder_tokens_per_q_time = builder_tokens / num_qa_times
        builder_time_per_q_time = builder_time / num_qa_times
        qa_tokens_per_q = f'{qa_tokens_per_q / 1000:.1f} + {builder_tokens_per_q_time / 1000:.1f}'
        qa_time_per_q = f'{qa_time_per_q:.1f} + {builder_time_per_q_time:.1f}'

    # Tree sizes
    sum_final_tree_size = 0
    sum_avg_tree_size = 0
    for history_id in history_ids:
        tree_file = exp_dir / history_id / 'tree-states.log'
        trees = [tree for tree, _ in load_incremental_tree_steps_from_logfile(tree_file)]
        sum_final_tree_size += _tree_size(trees[-1])
        sum_avg_tree_size += sum(_tree_size(t) for t in trees) / len(trees)
    final_tree_size_per_h = sum_final_tree_size / num_histories
    macro_avg_tree_size = sum_avg_tree_size / num_histories

    forgotten_ratio_per_round = _eval_relevant_forgotten_ratio(exp_dir, full_results, history_ids)

    r = lambda x: round(x, ndigits=1)
    rel_count = lambda counter, cat: counter[cat.name] / counter.total()
    get_s_cp = lambda counter: (rel_count(counter, BroadEmvOutputCategory.correct),
                                rel_count(counter, BroadEmvOutputCategory.partially_correct))

    s_c, s_p = get_s_cp(cat_counter)
    s_c_before, s_p_before = get_s_cp(cat_counter_before)
    s_c_after, s_p_after = get_s_cp(cat_counter_after)
    better = change_stats['better'] / num_pairs
    same = change_stats['same'] / num_pairs
    return (
        r(s_c * 100), r((s_c + s_p) * 100),
        r(better * 100), r(same * 100),
        r(s_c_before * 100), r((s_c_before + s_p_before) * 100),
        r(s_c_after * 100), r((s_c_after + s_p_after) * 100),
        r(final_tree_size_per_h), r(macro_avg_tree_size),
        qa_tokens_per_q if is_offline else r(qa_tokens_per_q / 1000), r(forgetting_tokens_per_h / 1000),
        qa_time_per_q if is_offline else r(qa_time_per_q), r(forgetting_time_per_h),
        r(forgotten_ratio_per_round[1] * 100), r(forgotten_ratio_per_round[2] * 100)
    )


def main():
    metrics = []
    for path in sys.argv[1:]:
        exp_dir = Path(path)
        metrics.append(eval_exp_dir(exp_dir))

    print(
        'QA S_c', 'QA S_p',
        'QA better', 'QA same',
        'QA S_c before', 'QA S_p before',
        'QA S_c after', 'QA S_p after',
        'final tree size', 'avg tree size',
        'QA tokens', 'forgetting tokens',
        'QA time', 'forgetting time',
        'forgotten ratio r1', 'forgotten ratio r2',
        sep=' & '
    )
    for metric_row in metrics:
        print(*metric_row, sep=' & ')


if __name__ == '__main__':
    main()
