import pickle
import sys
import time
import traceback
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from typing import Iterable, Dict, List, Tuple

from em.em_tree import HigherLevelSummary
from em.incremental_history import log_tree_state
from em.organize.forget import ForgettingManager
from em.organize.language_rule_relevance import LanguageRuleManager
from lmp.repl.code_execution import ReplExecutionEnvironment
from lmp.token_callback import get_token_tracking_callback
from .exp_feedback import ExperimentFeedbackManager
from .setup import setup_interactive_emv_lmp
from .utils import simplify_summary_node
from ..qa_eval import EpisodicQASample, EpisodicQAModelOutput

_global_shutdown_flag = False


def set_global_shutdown():
    global _global_shutdown_flag
    _global_shutdown_flag = True


def run_incremental_eval(
        forgetting_manager: ForgettingManager,
        history_iterator: Iterable[Tuple[HigherLevelSummary, str]],
        qa_dataset: Dict[datetime, List[EpisodicQASample]],  # history=None
        runner: 'ExperimentRunner',
        history_log_dir: Path,
        log_every_n_steps: int = 1,
        debug_skip_qa=False,
):
    tree_state_log = (history_log_dir / 'tree-states.log').open('w')
    if forgetting_manager:
        tree_state_log_before_forget = (history_log_dir / 'tree-states-before-forgetting.log').open('w')

    results = []
    time_qa, time_forgetting = 0, 0
    tokens_completion_forgetting, tokens_prompt_forgetting = 0, 0
    unused_keys = set(qa_dataset.keys())

    try:
        for i, (history, step_log_name) in enumerate(history_iterator):
            if _global_shutdown_flag:
                break
            ts = history.range[-1]

            # forgetting manager modifies the history in-place.
            # This actually modifies the (finalized) states of the incremental history builder so it will persist to the
            # next steps. The history builder only rebuilds the non-finalized "most recent" children frequently, which
            # should not be affected by the forgetting manager
            # Forgetting is done before QA since for full-state (offline) tree building, the history is initialized
            # with the full content at each step
            t = time.time()
            if forgetting_manager:
                if i % log_every_n_steps == 0:
                    # noinspection PyUnboundLocalVariable
                    log_tree_state(history, step_log_name, tree_state_log_before_forget)
                with get_token_tracking_callback() as cb:
                    forgetting_manager.modify(
                        history, ts  # Alternative: use max(s.question_time for s in samples) here?
                    )
                    tokens_prompt_forgetting += cb.prompt_tokens
                    tokens_completion_forgetting += cb.completion_tokens
            time_forgetting += (time.time() - t)

            if i % log_every_n_steps == 0:
                log_tree_state(history, step_log_name, tree_state_log)

            if ts in qa_dataset:
                (history_log_dir / f'{str(ts)}.history.pkl').write_bytes(pickle.dumps(history))
                unused_keys.remove(ts)
                samples = qa_dataset[ts]

                def _exec_sample(sample: EpisodicQASample):
                    if debug_skip_qa:
                        return EpisodicQAModelOutput.from_sample(sample, "I don't know"), 0

                    sys.stdout.set_log_for_current_thread(history_log_dir / f'{sample.sample_id}.out.log')
                    sys.stderr.set_log_for_current_thread(history_log_dir / f'{sample.sample_id}.err.log')
                    try:
                        my_runner = runner.thread_local_copy()
                        sample.history = simplify_summary_node(history)
                        t1 = time.time()
                        result = my_runner.safe_run_model(sample)  # this already includes interactive feedback handling
                        local_time_qa = time.time() - t1 - my_runner.time_wait_for_user_response
                        print('QA time:', local_time_qa,
                              'wait for user response:', my_runner.time_wait_for_user_response)
                        return result, local_time_qa
                    finally:
                        sys.stdout.close_log_for_current_thread()
                        sys.stderr.close_log_for_current_thread()

                pool = ThreadPoolExecutor(max_workers=min(len(samples), runner.max_parallel_qa_per_history),
                                          thread_name_prefix=f'inner-loop-{history_log_dir.name}')
                try:
                    result_with_times = list(pool.map(_exec_sample, samples))
                    results += [r for r, local_time_qa in result_with_times]
                    time_qa += sum(local_time_qa for r, local_time_qa in result_with_times)
                except KeyboardInterrupt:
                    print('Interrupted', history_log_dir.name)
                    break

            if len(unused_keys) == 0:
                # No questions to evaluate anymore => building history and forgetting would be wasted compute
                break

        if unused_keys:
            print('WARNING: Unused keys', unused_keys)
    except BaseException as e:
        print('Unexpected error while running', history_log_dir.name, ':', e)
        traceback.print_exc()
    finally:
        tree_state_log.close()
    # Always return results so far, even if there was some exception
    return results, (time_qa, time_forgetting, tokens_prompt_forgetting, tokens_completion_forgetting)


class ExperimentRunner:
    _serves_as_root_marker = object()

    def __init__(self,
                 history_id: str,
                 cfg_name: str,
                 language_rule_manager: LanguageRuleManager,
                 feedback_manager: ExperimentFeedbackManager,
                 max_parallel_qa_per_history: int = 100000):
        super().__init__()
        self.max_parallel_qa_per_history = max_parallel_qa_per_history
        self._history_id = history_id
        self._feedback_manager = feedback_manager
        self.cfg_name = cfg_name
        self.language_rule_manager = language_rule_manager
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self._most_recent_tts = None
        self._current_sample = None
        self._gave_feedback_for_current_sample = False  # Allow only one feedback, afterward end this conversation
        self.time_wait_for_user_response = 0
        self._parent = None

    def thread_local_copy(self) -> 'ExperimentRunner':
        self._parent = self._serves_as_root_marker
        copy = ExperimentRunner(self._history_id, self.cfg_name, self.language_rule_manager, self._feedback_manager)
        copy._parent = self
        return copy

    def safe_run_model(self, sample: EpisodicQASample):
        try:
            hypothesis = self.run_model(sample)
        except KeyboardInterrupt:
            raise
        except Exception as e:
            traceback.print_exc()
            hypothesis = '###ERROR### ' + str(e)
        return EpisodicQAModelOutput.from_sample(sample, hypothesis)

    def run_model(self, sample: EpisodicQASample):
        if self._parent == self._serves_as_root_marker:
            raise AssertionError('Runner that serves as parent cannot be used for experiment.')
        self._most_recent_tts = None
        self._gave_feedback_for_current_sample = False
        self._current_sample = sample
        self.time_wait_for_user_response = 0
        with get_token_tracking_callback() as cb:
            lmp = setup_interactive_emv_lmp(sample.history, sample.question_time, self.cfg_name,
                                            wait_for_trigger_callback=self._impl_wait_for_trigger,
                                            tts=self._impl_tts,
                                            language_rule_manager=self.language_rule_manager)
            result = lmp(sample.question)
            self.total_prompt_tokens += cb.prompt_tokens
            self.total_completion_tokens += cb.completion_tokens
            if self._parent:
                self._parent.total_prompt_tokens += cb.prompt_tokens
                self._parent.total_completion_tokens += cb.completion_tokens
            return result

    def _impl_tts(self, text: str):
        self._most_recent_tts = text
        print(f' -> System saying: "{text}"')

    def _impl_wait_for_trigger(self):
        print(f' -> System answer: "{self._most_recent_tts}"')
        t = time.time()
        try:
            if self._gave_feedback_for_current_sample:
                raise StopIteration((ReplExecutionEnvironment.RETURN_FN_SIGNAL, self._most_recent_tts))

            feedback = self._feedback_manager.ask_for_feedback(self._history_id, self._current_sample,
                                                               hyp=self._most_recent_tts)
            if not feedback.proceed:
                raise KeyboardInterrupt
            if feedback.feedback:
                self._gave_feedback_for_current_sample = True
                return {'type': 'dialog', 'text': feedback.feedback}
            else:
                raise StopIteration((ReplExecutionEnvironment.RETURN_FN_SIGNAL, self._most_recent_tts))

        finally:
            self.time_wait_for_user_response += (time.time() - t)
