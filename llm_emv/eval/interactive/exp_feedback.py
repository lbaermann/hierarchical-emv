import json
import sys
import time
from collections import namedtuple
from dataclasses import dataclass
from json import JSONDecodeError
from pathlib import Path
from queue import Queue
from threading import Condition
from typing import Callable, Optional

from wrapt import synchronized

from ..qa_eval import EpisodicQASample, EpisodicQAModelOutput


@dataclass
class _PendingExperimentFeedbackRequest:
    id: int
    output: EpisodicQAModelOutput

    @property
    def json(self):
        return {
            'req_id': self.id,
            'sample_id': self.output.sample_id,
            'q_time': self.output.question_time.strftime('%Y/%m/%d %H:%M:%S'),
            'q': self.output.question,
            'gt': self.output.answer,
            'hyp': self.output.hypothesis,
            'proceed': True,
            'feedback': None
        }


ExperimentFeedback = namedtuple('ExperimentFeedback',
                                ['proceed', 'feedback'])


class ExperimentFeedbackManager:
    auto_feedback_provider: Optional[Callable[[EpisodicQAModelOutput], ExperimentFeedback]]

    def __init__(self, max_running_experiments: int = 4,
                 feedback_file: Path = None):
        super().__init__()
        self._max_running_experiments = max_running_experiments
        self._pending_items: Queue[_PendingExperimentFeedbackRequest] = Queue()
        self._feedback_conditions = {}
        self._feedback_results = {}
        self._id_counter = 0
        self._running_experiment_history_ids = set()
        self._experiment_counter_condition = Condition()
        self._feedback_file = feedback_file
        self.auto_feedback_provider = None
        self.disable_feedback = False

    def start_experiment(self, history_id: str, _could_be_inner_loop=False):
        with self._experiment_counter_condition:
            if history_id in self._running_experiment_history_ids:
                if _could_be_inner_loop:
                    return
                else:
                    raise AssertionError(history_id)
            while len(self._running_experiment_history_ids) >= self._max_running_experiments:
                _print(f'Need to wait to run experiment {history_id}...')
                self._experiment_counter_condition.wait()
            _print(f'Running experiment {history_id}...')
            self._running_experiment_history_ids.add(history_id)

    def finished_experiment(self, history_id: str, _could_be_inner_loop=False):
        with self._experiment_counter_condition:
            if history_id not in self._running_experiment_history_ids:
                if _could_be_inner_loop:
                    return
                else:
                    raise AssertionError(history_id)
            self._running_experiment_history_ids.remove(history_id)
            self._experiment_counter_condition.notify_all()

    def ask_for_feedback(self, history_id: str, sample: EpisodicQASample, hyp: str) -> ExperimentFeedback:
        if self.disable_feedback:
            return ExperimentFeedback(proceed=True, feedback=None)
        if self.auto_feedback_provider:
            return self.auto_feedback_provider(EpisodicQAModelOutput.from_sample(sample, hyp))

        with synchronized(self):
            self._id_counter += 1
            my_id = self._id_counter
        condition = Condition()
        self._feedback_conditions[my_id] = condition
        _print(
            f'Suspending {sample.sample_id} ({my_id}). {len(self._running_experiment_history_ids) - 1} running, '
            f'{self._pending_items.qsize() + 1} suspended')
        self._pending_items.put(_PendingExperimentFeedbackRequest(
            my_id, EpisodicQAModelOutput.from_sample(sample, hyp)))
        self.finished_experiment(history_id, _could_be_inner_loop=True)  # Not really finished, but suspended

        with condition:
            while my_id not in self._feedback_results:
                condition.wait()
            del self._feedback_conditions[my_id]
            feedback = self._feedback_results.pop(my_id)
        self.start_experiment(history_id, _could_be_inner_loop=True)  # May need to wait
        _print(f'Resuming {my_id}')
        return feedback

    def _set_feedback(self, req_id: int, feedback: ExperimentFeedback):
        print('Sending feedback', req_id, ':', feedback)
        condition = self._feedback_conditions[req_id]
        with condition:
            self._feedback_results[req_id] = feedback
            condition.notify()

    def interactive_feedback_loop(self):
        while True:
            feedback_request = self._pending_items.get()
            req_id = feedback_request.id
            print(f'Feedback request {req_id}:')
            print('   ID:', feedback_request.output.sample_id)
            print('    Q:', feedback_request.output.question)
            print('   GT:', feedback_request.output.answer)
            print('  HYP:', feedback_request.output.hypothesis)
            choice = None
            while choice is None or choice not in 'FGA':
                choice = input(' -> (F)inish this sample, (G)ive feedback, (A)bort completely > ')
            if choice == 'F':
                self._set_feedback(req_id, ExperimentFeedback(proceed=True, feedback=None))
            elif choice == 'G':
                self._set_feedback(req_id, ExperimentFeedback(proceed=True, feedback=input('Feedback: > ')))
            elif choice == 'A':
                self._set_feedback(req_id, ExperimentFeedback(proceed=False, feedback=None))

    def abort_all_pending_requests(self):
        while self._pending_items.qsize():
            req = self._pending_items.get_nowait()
            self._set_feedback(req.id, ExperimentFeedback(proceed=False, feedback=None))

    def feedback_file_loop(self):
        while True:
            time.sleep(10)
            items_json = [x.json for x in self._pending_items.queue]
            items_json += [
                {'req_id': "### Remove this and rename to '.response' when the file can be processed ###"}
            ]
            self._feedback_file.write_text(json.dumps(items_json, indent=2))
            response_file = self._feedback_file.with_suffix('.response')
            if not response_file.is_file():
                continue
            print('Reading response file...')
            try:
                response_data: list = json.loads(response_file.read_text())
            except JSONDecodeError as e:
                print('Invalid JSON file:', str(e))
                continue
            response_ids = [x['req_id'] for x in response_data]
            pending_ids = [x.id for x in self._pending_items.queue]
            if response_ids != pending_ids:
                _print(f'Ignoring response file since ids do not match. expected: {pending_ids}')
                continue
            response_file.rename(
                response_file.with_stem(f'feedback-{int(time.time() * 1000)}').with_suffix('.processed.json'))
            while self._pending_items.qsize():
                item = self._pending_items.get_nowait()
                for x in response_data:
                    if x['req_id'] == item.id:
                        self._set_feedback(item.id,
                                           ExperimentFeedback(proceed=x['proceed'], feedback=x['feedback']))


def _print(s: str):
    # noinspection PyArgumentList
    sys.stdout.write(s + '\n', force_console=True)
