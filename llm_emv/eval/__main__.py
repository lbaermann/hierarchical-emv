import argparse
from datetime import datetime
from functools import partial
from pathlib import Path

from em.em_tree import HigherLevelSummary
from lmp.repl.code_execution import ReplExecutionEnvironment
from lmp.token_callback import get_token_tracking_callback
from .datasets import add_dataset_args_and_parse
from .qa_eval import run_evaluation, write_results
from ..setup import setup_llm_emv

total_prompt_tokens, total_completion_tokens = 0, 0


def run_model(cfg: str, question: str, question_time: datetime, history: HigherLevelSummary) -> str:
    global total_prompt_tokens, total_completion_tokens

    def _exit_lmp_on_wait_for_trigger():
        raise StopIteration((ReplExecutionEnvironment.RETURN_FN_SIGNAL, None))

    def _exit_lmp_and_report_output(s: str):
        raise StopIteration((ReplExecutionEnvironment.RETURN_FN_SIGNAL, s))

    with get_token_tracking_callback() as cb:
        lmp = setup_llm_emv(cfg, history, now_time=question_time,
                            wait_for_trigger_callback=_exit_lmp_on_wait_for_trigger,
                            tts=_exit_lmp_and_report_output)
        output = lmp(question)
        print(cb)
        total_prompt_tokens += cb.prompt_tokens
        total_completion_tokens += cb.completion_tokens

    return output


def main():
    from langchain_community.cache import SQLiteCache
    import langchain.globals
    langchain.globals.set_llm_cache(SQLiteCache(database_path="langchain-cache.db"))
    langchain.globals.set_verbose(True)

    parser = argparse.ArgumentParser()
    parser.add_argument('--cfg', type=str, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--only-iter-dataset', action='store_true', default=False,
                        help='Only iter through the dataset. Useful if the dataset does '
                             'some preprocessing and caching.')
    args, dataset = add_dataset_args_and_parse(parser)

    assert not args.output.is_file(), str(args.output)
    if args.only_iter_dataset:
        print('\n!!! ONLY ITERATING DATASET, NOT PERFORMING EVAL !!!\n')
        for i, sample in enumerate(dataset):
            print('\n\nLoaded sample', i, sample.sample_id)
        return

    result = run_evaluation(partial(run_model, args.cfg), dataset)
    write_results(result, args, args.output, token_costs={
        'prompt_tokens': total_prompt_tokens,
        'completion_tokens': total_completion_tokens,
    })


if __name__ == '__main__':
    main()
