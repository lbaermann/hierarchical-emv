import argparse
# noinspection PyUnresolvedReferences
import readline
from pathlib import Path

from llm_emv.emv_api import EMVerbalizationAPI
from llm_emv.eval.dechant_qa_dataset import TeachDeChantDataset
from llm_emv.interactive_tree import recursive_apply, ExpandableList
from llm_emv.setup import create_search_embedding_and_cfg, setup_namespace
from lmp.repl.code_execution import ReplExecutionEnvironment

_multi_ep_q_types = [
    'exact_time_to_episode',
    'seq_right_after_questions',
    'seq_right_before_questions',
    'seq_simple_object_yes_no',
    'seq_specific_shortened_low_actions',
    'sequence_of_task_descs',
    'tasks_to_days_ago',
    'tasks_to_exact_times',
    'days_ago_to_episode',
    'seq_low_actions_to_episode_task_descs',
]

_single_ep_q_types = [
    'action_either_or',
    'game_desc',
    'low_actions',
    'object_either_or',
    'right_after_questions',
    'right_before_questions',
    'simple_action_yes_no',
    'simple_object_yes_no'
]


def _set_simplified_repr(node):
    node._simplified_repr = True


def interactive_create_samples():
    parser = argparse.ArgumentParser(description='Interactively create prompts from teach-dechant train data')
    parser.add_argument('--num-samples-per-type', type=int, default=2, metavar='N')
    parser.add_argument('--single-ep-mode', default=False, action='store_true')
    parser.add_argument('--skip-existing', default=False, action='store_true')
    parser.add_argument('--hierarchy-level', default='deep',
                        choices=['deep', 'predefined', 'predefined+', 'none'])
    TeachDeChantDataset.add_argparse_args(parser)
    args = parser.parse_args()

    question_types = _single_ep_q_types if args.single_ep_mode else _multi_ep_q_types
    search_emb, search_cfg = create_search_embedding_and_cfg({})

    ep_id = 0
    for q_type in question_types:
        dataset = TeachDeChantDataset.from_argparse_args(args, samples_per_episode=1,
                                                         filter_by_question_types=(q_type,))
        for n in range(args.num_samples_per_type):

            out_file = Path(__file__).parent / f'qa.{q_type}.{n}.prompt.py'
            if out_file.is_file() and args.skip_existing:
                print('Skipping existing file', out_file)
                ep_id += 1
                continue

            for i, sample in enumerate(dataset):
                if i < ep_id:
                    continue  # Use each episode only once

                try:
                    _handle_sample(n, q_type, sample, search_cfg, search_emb, args.hierarchy_level)
                except KeyboardInterrupt:
                    return
                ep_id += 1
                break


def _handle_sample(n, q_type, sample, search_cfg, search_emb, hierarchy_level):
    out_file = Path(__file__).parent / f'qa.{q_type}.{n}.prompt.py'
    if out_file.is_file():
        print('!!!\n!!! Sample file already exists!', out_file, '\n!!!')

    answer = None

    def tts(s):
        nonlocal answer
        answer = s

    # noinspection PyTypeChecker
    api = EMVerbalizationAPI(wait_for_trigger=None, tts=tts, history=sample.history,
                             now_time=sample.question_time, hierarchy_level=hierarchy_level,
                             vlm=None, search_embedding_fn=search_emb, search_filter_kwargs=search_cfg)
    exec_env = ReplExecutionEnvironment(setup_namespace(api))
    recursive_apply(api.history, _set_simplified_repr)

    cmd_history = []
    state_history = []  # history _before_ cmd at the same index
    result_history = []  # result of cmd at the same index, only non-tree results
    while answer is None:
        state_history.append(repr(api.history))
        print('Q:', sample.question)
        print('A:', sample.answer)
        print(api.history)
        try:
            cmd = input('>>> ')
            if not cmd.strip():
                continue
            if cmd == 'restart':
                cmd_history.clear()
                state_history.clear()
                result_history.clear()
                api.history.collapse_deep()
                print('\nRestarting\n')
                continue
            if cmd == 'skip':
                return

            results = exec_env(cmd)
            for r in results:
                if not isinstance(r, ExpandableList):
                    print(r)
            cmd_history.append(cmd)
            result_history.append([repr(r) for r in results
                                   if not (r is None or isinstance(r, ExpandableList))])
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except:
            pass

    prompt = "User question: " + sample.question + "\n\n"
    for cmd, state_before, results in zip(cmd_history, state_history, result_history):
        prompt += state_before + '\n\n'
        prompt += f'>>> {cmd}\n'
        for r in results:
            prompt += r + '\n'
        prompt += '\n'

    out_file.write_text(prompt)
    print('Written', out_file)


def main():
    import langchain.globals
    import langchain_community.callbacks
    from langchain_community.cache import SQLiteCache
    langchain.globals.set_llm_cache(SQLiteCache(database_path="langchain-cache.db"))
    langchain.globals.set_verbose(True)

    with langchain_community.callbacks.get_openai_callback() as cb:
        try:
            interactive_create_samples()
        finally:
            print(cb)


if __name__ == '__main__':
    main()
