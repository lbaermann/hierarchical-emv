import ast
import json
import traceback
from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path
from typing import List

from langchain_core.language_models import BaseLanguageModel
from langchain_core.output_parsers import JsonOutputParser

from em.em_tree import HigherLevelSummary
from llm_emv.eval.dechant_qa_dataset import TeachDeChantDataset
from llm_emv.eval.qa_eval import EpisodicQASample, EpisodicQAModelOutput
from llm_emv.eval.util import determine_git_commit
from llm_emv.zs_flat_history_qa import ZeroShotOnePassSemiFlatQA
from lmp.setup import instantiate_llm
from lmp.util import llm_predict

_zs_teach_batch_prompt = '''You are a smart humanoid robot answering user questions about your past actions.
You are given a history that contains information on what you did in the past.
Carefully inspect the content of the history to answer the given questions.

History:
{history}
Current time: {now}

Questions:
{question_json}

Answer with a JSON of the form 
{{
    "question_id": {{
        "reasoning": "1-2 sentences",
        "answer": "compact answer"
    }}, 
    ...
}}
Make sure to answer every question exactly once!'''  # Double {{ are because this is a template string


class ZeroShotBatchHistoryQA:

    def __init__(self, llm: BaseLanguageModel):
        super().__init__()
        self.llm = llm
        self.prompt = _zs_teach_batch_prompt
        self.include_lowest_level_details = True
        self.total_prompt_tokens = 0

    def __call__(self, history: HigherLevelSummary, q_time: datetime, questions: List[str]):
        # noinspection PyTypeChecker
        history_str = ZeroShotOnePassSemiFlatQA._format_history_l1(self, history)
        history_str = (history_str
                       .replace('Goal: ', '')
                       .replace('Action: ', ''))

        prompt = self.prompt.format(history=history_str, question_json=json.dumps({
            f'question_{i}': q
            for i, q in enumerate(questions)
        }), now=q_time.strftime('%Y-%m-%d %H:%M:%S'))

        if 'ChatGoogleGenerativeAI' in self.llm.__class__.__name__:
            token_count = self.llm.client.count_tokens({
                'model': self.llm.model,
                'contents': [{'parts': [{
                    'text': prompt
                }]}]
            })
            print('Manual token count estimate:', token_count.total_tokens)
            self.total_prompt_tokens += token_count.total_tokens

        print('\n==== Prompting: ==== \n', prompt, '\n===============\n')
        response = llm_predict(self.llm, prompt)
        print('LLM Response:\n', response, '\n\n')

        result = {}
        parsed = JsonOutputParser().parse(response)
        for sample_id, sample_result in parsed.items():
            if isinstance(sample_id, str) and sample_id.startswith('question_'):
                sample_id = sample_id[len('question_')]
            i = int(sample_id)
            result[i] = sample_result['answer']
        return [result[i] for i in range(len(result))]


def _batch_iter(dataset: TeachDeChantDataset):
    for trial_ids in dataset._qa_data.keys():
        for b, batch in enumerate(dataset._qa_data[trial_ids]):
            # noinspection PyTypeChecker
            history = dataset._load_history(batch, start_time=None)
            samples_for_history = []

            for key, value in batch.items():
                if key in dataset._non_question_keys():
                    continue
                assert (isinstance(value, dict)
                        and 'text_input' in value
                        and 'target_output' in value), f'key={key}, value={value}'
                q, a = value['text_input'], value['target_output']
                sample_id = f'{"-".join(trial_ids)}-{b}-{key}'
                q_time = batch['now_time_stamp']
                samples_for_history.append(EpisodicQASample(sample_id, q, q_time, a, history))

            yield history, samples_for_history


def main():
    from langchain_community.cache import SQLiteCache
    import langchain.globals
    langchain.globals.set_llm_cache(SQLiteCache(database_path="langchain-cache.db"))
    langchain.globals.set_verbose(True)

    parser = ArgumentParser()
    TeachDeChantDataset.add_argparse_args(parser)
    parser.add_argument('--n-batches', type=int, default=None)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--llm', type=ast.literal_eval, required=True)
    args = parser.parse_args()

    if args.output.is_file():
        raise FileExistsError(args.output)

    llm = instantiate_llm(args.llm)
    model = ZeroShotBatchHistoryQA(llm)
    dataset = TeachDeChantDataset.from_argparse_args(args)

    result = []
    for i, (history, samples_for_history) in enumerate(_batch_iter(dataset)):
        if args.n_batches is not None and i >= args.n_batches:
            break

        try:
            print('Evaluating samples', [s.sample_id for s in samples_for_history])
            answers = model(history, samples_for_history[0].question_time,
                            [sample.question for sample in samples_for_history])
            for sample, answer in zip(samples_for_history, answers):
                result.append(EpisodicQAModelOutput(hypothesis=answer, **sample.__dict__))
        except KeyboardInterrupt:
            break
        except Exception as e:
            traceback.print_exc()

    args.output.write_text(json.dumps({
        'config': {k: str(v) for k, v in args.__dict__.items()},
        'code_commit': determine_git_commit(),
        'results': {
            r.sample_id: {
                'q_time': r.question_time.strftime('%Y/%m/%d %H:%M:%S'),
                'q': r.question,
                'gt': r.answer,
                'hyp': r.hypothesis
            }
            for r in result
        },
        'gemini_costs': {
            'prompt_tokens': model.total_prompt_tokens,
        }
    }, indent=2))


if __name__ == '__main__':
    main()
