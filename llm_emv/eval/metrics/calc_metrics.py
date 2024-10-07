import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from pprint import pprint
from typing import List, Dict

from nltk.translate.meteor_score import meteor_score
from rouge_score.rouge_scorer import RougeScorer
from rouge_score.tokenize import tokenize
from sacrebleu.metrics import BLEU, BLEUScore

from .categories import BroadEmvOutputCategory, FineEmvOutputCategory


def _calc_meteor(predictions: List[str], gold_annotations: List[List[str]]):
    total = 0
    for pred, possible_refs in zip(predictions, gold_annotations):
        pred = tokenize(pred, None)  # TODO check tokenization
        # https://github.com/cmu-mtlab/meteor/blob/master/src/edu/cmu/meteor/util/Normalizer.java
        possible_refs = [tokenize(x, None) for x in possible_refs]
        total += meteor_score(possible_refs, pred)
    return total / len(predictions)


def _calc_rouge(predictions: List[str], gold_annotations: List[List[str]]) -> Dict[str, Dict[str, float]]:
    rouge_scorer = RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=False)
    rouge = defaultdict(lambda: defaultdict(lambda: 0.0))
    for pred, possible_refs in zip(predictions, gold_annotations):
        sample_result = {}
        for ref in possible_refs:
            single_ref_result = rouge_scorer.score(ref, pred)
            for k, scores in single_ref_result.items():
                existing_result_dict = sample_result.setdefault(k, {})
                if existing_result_dict.get('f', -1) < scores.fmeasure:
                    existing_result_dict.update(f=scores.fmeasure, p=scores.precision, r=scores.recall)
        for k, best_scores in sample_result.items():
            rouge[k]['p'] += best_scores['p']
            rouge[k]['r'] += best_scores['r']
            rouge[k]['f'] += best_scores['f']
    return {
        rouge_type: {
            measure: score / len(predictions)
            for measure, score in results.items()
        } for rouge_type, results in rouge.items()
    }


def _calc_bleu(predictions: List[str], gold_annotations: List[List[str]]) -> Dict[str, float]:
    refs_transposed = [
        [refs[i] for refs in gold_annotations]
        for i in range(len(gold_annotations[0]))
    ]
    bleu: BLEUScore = BLEU().corpus_score(predictions, refs_transposed)
    return {
        'BLEU': bleu.score,
        'BLEU.bp': bleu.bp,
        'BLEU.ratio': bleu.ratio,
        'BLEU.hyp_len': float(bleu.sys_len),
        'BLEU.ref_len': float(bleu.ref_len),
    }


def _category_eval(results):
    categories = Counter()
    for result in results:
        if 'cat' in result:
            categories.update([result['cat']])

    def _print_categories():
        max_key_len = max(len(k) for k in categories.keys())
        for k, v in sorted(categories.items()):
            print(k.rjust(max_key_len), f': {v: >3} ({v / len(results): >6.1%})')

    if categories:
        if any(k not in BroadEmvOutputCategory.all_names() for k in categories.keys()):
            print('\nFine Categories:')
            _print_categories()
            broad_categories = Counter()
            for k, v in categories.items():
                broad_categories.update({FineEmvOutputCategory(k).broad.name: v})
            categories = broad_categories
        print('\nBroad Categories:')
        _print_categories()
        return [categories[BroadEmvOutputCategory.correct.name] / len(results) * 100,
                categories[BroadEmvOutputCategory.partially_correct.name] / len(results) * 100]
    return []


def _surface_eval(results):
    hypotheses = [r['hyp'] for r in results]
    ground_truths = [[r['gt']] for r in results]

    correct = 0
    for hyp, gt in zip(hypotheses, ground_truths):
        if hyp == gt[0]:
            correct += 1

    blue_dict = _calc_bleu(hypotheses, ground_truths)
    rouge_dicts = _calc_rouge(hypotheses, ground_truths)
    meteor = _calc_meteor(hypotheses, ground_truths)

    print('BLEU')
    pprint(blue_dict)

    print('\nROUGE')
    pprint(rouge_dicts)

    print('\nMETEOR:', meteor, '\n')
    total = len(hypotheses)

    print('Total:', total)
    print('Exact matches:', correct)
    print(f'Plain Accuracy: {correct / total:.2%}')

    return [blue_dict['BLEU'], rouge_dicts['rougeL']['f'] * 100]


def main():
    exp_output_file = Path(sys.argv[1])
    exp_output = json.loads(exp_output_file.read_text())

    metric_latex_line = []
    results = exp_output['results'].values()
    if all('gt' in r for r in results):
        metric_latex_line += _surface_eval(results)

    if any('cat' in r for r in results):
        metric_latex_line += _category_eval(results)
    else:
        auto_eval_files = list(exp_output_file.parent.glob(f'{exp_output_file.stem}.*.auto_eval.json'))
        if len(auto_eval_files) == 1:
            print('\nReading auto-eval from', auto_eval_files[0])
            auto_eval_data = json.loads(auto_eval_files[0].read_text())
            metric_latex_line += _category_eval(auto_eval_data['results'].values())
        elif len(auto_eval_files) > 1:
            print('Multiple auto-eval files found, unclear which one to consider. Pass it separately.')

    cost_keys = [k for k in exp_output.keys() if k.endswith('_costs')]
    if len(cost_keys) == 1:
        prompt_tokens = exp_output[cost_keys[0]]['prompt_tokens']
        token_per_sample = prompt_tokens / len(results)
        print('Token cost per sample: ', token_per_sample)
        metric_latex_line += [token_per_sample / 1000]
    elif len(cost_keys) > 1:
        print('\n!!!\nWARNING: Multiple cost keys found. Not sure which one to consider!', cost_keys, '\n!!!\n')

    print('\nLaTeX table entry:')
    print('B & R & $S_c$ & $S_p$ & T ')
    print(' & '.join(format(x, f'>3.{0 if i in [2, 3] else 1}f') for i, x in enumerate(metric_latex_line)))


if __name__ == '__main__':
    main()
