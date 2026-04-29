import argparse
import ast
import sys
import time
import traceback
from argparse import ArgumentParser, Namespace
from concurrent.futures.thread import ThreadPoolExecutor
from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path
from threading import Thread
from typing import List, Tuple, Dict, Type

from langchain_core.language_models import BaseChatModel
from wrapt import synchronized

from em.organize.forget import ForgettingManager
from em.organize.language_rule_relevance import LanguageRuleBasedRelevanceEstimator, LanguageRuleManager
from lmp.setup import instantiate_llm
from .data.armarx import ArmarXHistorySeqDataset
from .data.base import HistorySequenceQaDataset, OnlyFirstNSamplesDataset
from .data.teach import TeachHistorySequenceSceneIncrementalDataset, TeachHistorySequenceFullStateDataset
from .exp_auto_feedback import AlwaysAutoFeedbackProvider, OnlyIfForgottenLLMAutoFeedbackProvider
from .exp_feedback import ExperimentFeedbackManager
from .exp_runner import ExperimentRunner, run_incremental_eval, set_global_shutdown
from .utils import SysRedirectPerThread
from ..qa_eval import EpisodicQAModelOutput, write_results


@dataclass
class _ExperimentResultsAndStats:
    results: List[EpisodicQAModelOutput] = field(default_factory=lambda: [])

    total_time_builder: float = 0
    total_time_qa: float = 0
    total_time_forgetting: float = 0

    qa_prompt_tokens: int = 0
    qa_completion_tokens: int = 0
    forgetting_prompt_tokens: int = 0
    forgetting_completion_tokens: int = 0

    @synchronized
    def update_from(self, results: List[EpisodicQAModelOutput],
                    time_token_stats: Tuple[float, float, int, int],
                    exp_runner: ExperimentRunner):
        time_qa, time_forgetting, forgetting_prompt_tokens, forgetting_completion_tokens = time_token_stats
        self.results += results
        self.total_time_qa += time_qa
        self.total_time_forgetting += time_forgetting
        self.qa_prompt_tokens += exp_runner.total_prompt_tokens
        self.qa_completion_tokens += exp_runner.total_completion_tokens
        self.forgetting_prompt_tokens += forgetting_prompt_tokens
        self.forgetting_completion_tokens += forgetting_completion_tokens

    @property
    def token_costs(self):
        return {
            'qa': {
                'prompt_tokens': self.qa_prompt_tokens,
                'completion_tokens': self.qa_completion_tokens,
            },
            'forgetting': {
                'prompt_tokens': self.forgetting_prompt_tokens,
                'completion_tokens': self.forgetting_completion_tokens,
            },
        }

    @property
    def time_stats(self):
        return {
            'qa': self.total_time_qa,
            'forgetting': self.total_time_forgetting,
        }


def _perform_experiment_with_sample(args, sample, result: _ExperimentResultsAndStats,
                                    feedback_manager: ExperimentFeedbackManager):
    history_id, history_iterator, qa_samples = sample
    history_output_dir: Path = args.output_dir / history_id
    history_output_dir.mkdir(exist_ok=True)
    sys.stdout.set_log_for_current_thread(history_output_dir / 'stdout.log')
    sys.stderr.set_log_for_current_thread(history_output_dir / 'stderr.log')

    # noinspection PyTypeChecker
    language_rule_llm: BaseChatModel = instantiate_llm(args.language_rule_llm) if args.language_rule_llm else None
    # noinspection PyTypeChecker
    language_rule_mod_llm: BaseChatModel = instantiate_llm(args.language_rule_mod_llm
                                                           ) if args.language_rule_mod_llm else None
    if language_rule_mod_llm is None:
        language_rule_mod_llm = language_rule_llm
    if language_rule_mod_llm:
        language_rule_file = args.output_dir / history_id / 'language-rules.json'
        if language_rule_file.is_file():
            assert args.delete_language_rule_files, f'{language_rule_file} exists!'
            language_rule_file.unlink()
        language_rule_manager = LanguageRuleManager(language_rule_file, language_rule_mod_llm)
    else:
        language_rule_manager = None

    estimators = []
    if language_rule_llm is not None:
        language_rule_estimator = LanguageRuleBasedRelevanceEstimator(
            estimation_llm=language_rule_llm,
            rule_manager=language_rule_manager,
            ignore_raw_data=True  # To speed up evaluation – raw data is never relevant in simulated eval
        )
        estimators.append(language_rule_estimator)
    forgetting_manager = ForgettingManager(relevance_estimators=estimators, **args.forgetting_kwargs
                                           ) if args.forgetting_kwargs is not None else None
    exp_runner = ExperimentRunner(history_id, args.cfg, language_rule_manager, feedback_manager,
                                  args.max_parallel_qa_per_history)

    history_results, time_token_stats = run_incremental_eval(
        forgetting_manager, history_iterator, qa_samples, exp_runner,
        history_output_dir, args.log_every_n_steps, args.debug_skip_qa)
    result.update_from(history_results, time_token_stats, exp_runner)


def _add_dataset_args_and_parse(parser: ArgumentParser) -> Tuple[Namespace, HistorySequenceQaDataset]:
    dataset_classes: Dict[str, Type[HistorySequenceQaDataset]] = {
        'teach-scene': TeachHistorySequenceSceneIncrementalDataset,
        'teach-full': TeachHistorySequenceFullStateDataset,
        'armarx': ArmarXHistorySeqDataset,
    }
    parser.add_argument('--dataset-type', choices=dataset_classes.keys(), required=True)
    parser.add_argument('--n-samples', type=int, default=None,
                        help='Use only the first n samples from the dataset')

    args, _ = parser.parse_known_args()
    dataset_cls = dataset_classes[args.dataset_type]
    dataset_cls.add_argparse_args(parser)
    args = parser.parse_args()

    dataset = dataset_cls.from_argparse_args(args)
    if args.n_samples:
        dataset = OnlyFirstNSamplesDataset(dataset, args.n_samples)
    return args, dataset


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cfg', default='teach/paper')
    parser.add_argument('--language-rule-llm', type=ast.literal_eval, default=None,
                        help='LLM for language rule relevance estimation. '
                             'None to disable relevance estimation for tree building.')
    parser.add_argument('--language-rule-mod-llm', type=ast.literal_eval, default=None,
                        help='LLM for language rule manager. None uses --language-rule-llm by default.')
    parser.add_argument('--delete-language-rule-files', action='store_true', default=False)
    parser.add_argument('--forgetting-kwargs', type=ast.literal_eval, default={},
                        help='Supply "None" to completely turn off forgetting')
    parser.add_argument('--debug-skip-qa', action='store_true', default=False)
    parser.add_argument('--log-every-n-steps', type=int, default=1)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--max-running-experiments', type=int, default=4,
                        help='Max number of history iterators that may run in parallel. '
                             'If one stops to wait for feedback, other loaded ones may continue.')
    parser.add_argument('--max-loaded-experiments', type=int, default=None,
                        help='Max number of history iterators that may be loaded in parallel, i.e. thread pool size')
    parser.add_argument('--max-parallel-qa-per-history', type=int, default=100000,
                        help='History-specific thread pool size at QA time')
    parser.add_argument('--feedback-file', type=Path, default=None)
    parser.add_argument('--feedback-type', choices=[
        'file', 'tty', 'auto-llm', 'auto-always', 'none'
    ], default='file')
    parser.add_argument('--feedback-llm', type=ast.literal_eval, default=None,
                        help='LLM used for auto feedback response cl7u8 assification')

    args, dataset = _add_dataset_args_and_parse(parser)

    pool = ThreadPoolExecutor(thread_name_prefix='exp_runner',
                              max_workers=args.max_loaded_experiments)
    manager = ExperimentFeedbackManager(max_running_experiments=args.max_running_experiments,
                                        feedback_file=args.feedback_file or args.output_dir / 'feedback.json')
    if args.feedback_type == 'tty':
        Thread(target=manager.interactive_feedback_loop, name='interactive_feedback_loop', daemon=True).start()
    elif args.feedback_type == 'file':
        Thread(target=manager.feedback_file_loop, name='feedback_file_loop', daemon=True).start()
    elif args.feedback_type == 'auto-always':
        manager.auto_feedback_provider = AlwaysAutoFeedbackProvider()
    elif args.feedback_type == 'auto-llm':
        assert args.feedback_llm
        feedback_llm = instantiate_llm(args.feedback_llm)
        # noinspection PyTypeChecker
        manager.auto_feedback_provider = OnlyIfForgottenLLMAutoFeedbackProvider(feedback_llm)
    elif args.feedback_type == 'none':
        manager.disable_feedback = True
    else:
        raise NotImplementedError(args.feedback_type)

    SysRedirectPerThread.initialize()
    results = _ExperimentResultsAndStats()
    for sample in dataset:
        history_id = sample[0]
        time.sleep(1)

        def _run(hist_id, *run_args):
            # Important: Do not use captured loop variables here, esp. use hist_id instead of history_id
            try:
                manager.start_experiment(hist_id)  # This may need to wait until an execution slot is free
                print('Starting', hist_id, file=sys.stdout.terminal)
                _perform_experiment_with_sample(*run_args)
            except BaseException as e:
                traceback.print_exc(file=sys.stderr.terminal)
                print('ERROR', hist_id, ':', e, file=sys.stderr.terminal)
            finally:
                print('Finished', hist_id, file=sys.stdout.terminal)
                manager.finished_experiment(hist_id)
                sys.stdout.flush()
                sys.stderr.flush()

        # noinspection PyTypeChecker
        pool.submit(_run, history_id, deepcopy(args), sample, results, manager)
    try:
        pool.shutdown(wait=True, cancel_futures=False)
    except KeyboardInterrupt:
        print('Setting global shutdown flag')
        manager.abort_all_pending_requests()
        set_global_shutdown()
        try:
            print('Waiting for all tasks to exit...')
            pool.shutdown(wait=True, cancel_futures=True)
            print('All tasks done')
        except KeyboardInterrupt:
            print('Cancelled waiting')

    write_results(results.results, args, out_file=args.output_dir / 'results.json',
                  times={'builder': dataset.total_time_builder, **results.time_stats},
                  token_costs={'builder': dataset.builder_token_costs, **results.token_costs})


if __name__ == '__main__':
    import langchain.globals
    from langchain_community.cache import SQLiteCache

    langchain.globals.set_debug(True)
    langchain.globals.set_llm_cache(SQLiteCache(database_path="langchain-cache.db"))
    try:
        main()
    finally:
        # Make sure all redirected substreams are properly flushed and closed
        sys.stdout.close()
        sys.stderr.close()
