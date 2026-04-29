import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Iterable

import yaml
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.example_selectors import MaxMarginalRelevanceExampleSelector
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import HumanMessagePromptTemplate, SystemMessagePromptTemplate, \
    FewShotChatMessagePromptTemplate, AIMessagePromptTemplate
from langchain_core.runnables import Runnable, RunnablePassthrough

from em.incremental_history import format_rel_date
from lmp.setup import instantiate_llm
from .categories import FineEmvOutputCategory
from ..util import determine_git_commit


def create_llm_evaluator(llm: BaseChatModel,
                         similarity_model: str,
                         few_shot_k=5,
                         sample_files: Iterable[Path] = (),
                         use_broad_labels=False):
    sample_template = HumanMessagePromptTemplate.from_template('q: "{q}". gt: "{gt}". hyp: "{hyp}"')
    sample_template_with_ref_ts = HumanMessagePromptTemplate.from_template(
        'q: "{q}". gt: "{gt}". hyp: "{hyp}".'
        'GT reference time span: {ref_ts}'
    )

    embeddings = HuggingFaceEmbeddings(
        model_name=similarity_model
    )
    example_db = []
    for sample_file in sample_files:
        file_data = json.loads(sample_file.read_text())
        for sample in file_data['results'].values():
            example_db.append(dict(
                q=sample['q'],
                gt=sample['gt'],
                hyp=sample['hyp'],
                cat=(
                    FineEmvOutputCategory(sample['cat']).broad.name if use_broad_labels
                    else FineEmvOutputCategory(sample['cat']).name
                )
            ))
    print('Loaded few-shot sample db of size', len(example_db))
    if len(example_db):
        example_selector = MaxMarginalRelevanceExampleSelector.from_examples(
            examples=example_db,
            input_keys=['q', 'gt', 'hyp'],
            embeddings=embeddings,
            k=few_shot_k,
            vectorstore_cls=Chroma,
            collection_name='LlmEmvEvaluator'  # To not clash with other (in-memory) usages of Chroma
        )
        few_shot_prompt = FewShotChatMessagePromptTemplate(
            input_variables=['q', 'gt', 'hyp'],
            example_selector=example_selector,
            example_prompt=(
                    sample_template
                    + AIMessagePromptTemplate.from_template("{cat}")
            ),
        )
    else:
        few_shot_prompt = []

    cat_descriptions = '''
correct: The hypothesis is correct, or a correctly summarized version of the GT. It is also correct if hyp contains extra information that is most likely correct.
partially_correct: Parts of hyp are correct, parts are missing or wrong.
wrong: hyp is wrong or no answer at all.
'''.strip() if use_broad_labels else '''
correct: The hypothesis is correct (given the ground-truth answer and considering the question).
correct_summarized: information in hyp is correct, but a summarized version of GT
correct_tmi: information in hyp is correct, but there is additional (likely correct) information that is not in GT.
partially_correct_tmi: Parts of hyp are correct, parts are extra information that appears to be wrong given GT and the question
partially_correct_missing: Parts of hyp are correct, but important parts of GT are missing
wrong: hyp is wrong (but still a theoretically plausible answer to the question)
no_answer: the model refused to answer, stated it does not have enough information, or threw an error     
'''.strip()

    prompt = (
            SystemMessagePromptTemplate.from_template(
                f'''
Your task is to evaluate samples into the the following categories:

{cat_descriptions}

When a question is about time, a small offset can still be rated as correct.
Also consider the GT reference time span provided with the sample to assess whether a small offset is correct, partially_correct_missing or wrong.
When the question asks for a list of something (actions, objects, ...), compare the GT and hyp lists carefully.
If they match (modulo different specificity for object instance names or object quantities), its correct. 
If everything from hyp is in GT but hyp is missing some items from GT, it's partially_correct_missing.
If everything from GT is in hyp but hyp has some additional items, it's partially_correct_tmi (ignore the agent's hand).
If there is additional info different from listing items (e.g. specifiying object placement), but otherwise it's correct, use correct_tmi. 
Otherwise, it's wrong (even if there is some partial overlap). As soon as each list has one item that the other does not have, it's wrong.
You can rate a list answer correct_summarized if it has every item, but some are reasonably summarized (if it is not too broad). 

Output only a single category identifier, no reasoning or other sentence.
            '''.strip())
            + few_shot_prompt
            + sample_template_with_ref_ts
    )
    dtp = lambda s: datetime.strptime(s, '%Y/%m/%d %H:%M:%S')
    return RunnablePassthrough.assign(
        hyp=lambda d: '< no answer >' if d['hyp'] is None else d['hyp'],
        ref_ts=lambda d: (format_rel_date(None, dtp(d['ref_ts'][0][0]))
                          + ' - ' + format_rel_date(dtp(d['ref_ts'][0][0]), dtp(d['ref_ts'][0][1]))
                          if d['ref_ts'] else '-')
    ) | prompt | llm | StrOutputParser()


def _load_eval_chain_from_cfg(eval_cfg_file: Path) -> Runnable[dict, str]:
    cfg = yaml.safe_load(eval_cfg_file.read_text())
    sample_path: Path
    cfg['sample_files'] = [
        Path(sample_path) if Path(sample_path).is_absolute()
        else (eval_cfg_file.parent / sample_path).resolve()
        for sample_path in cfg.pop('samples', [])
    ]

    # noinspection PyTypeChecker
    return create_llm_evaluator(instantiate_llm(cfg.pop('llm', {})), **cfg)


def llm_eval(eval_cfg_file: Path, result_file: Path, eval_chain: Runnable[dict, str]):
    result_data = json.loads(result_file.read_text())
    samples = [dict(key=k, **v) for k, v in list(result_data['results'].items())[:10]]
    categories = eval_chain.batch(samples)
    result_map = {
        sample['key']: {'cat': cat}
        for sample, cat in zip(samples, categories)
    }
    git_commit = determine_git_commit()
    cfg_name = eval_cfg_file.stem
    output_file_suffix = f'.{cfg_name}-{git_commit[:6]}.auto_eval.json'
    result_file.with_suffix(output_file_suffix).write_text(json.dumps({
        'config': str(eval_cfg_file),
        'code_commit': git_commit,
        'results': result_map
    }, indent=2))


def main():
    import langchain.globals
    import langchain_community.callbacks
    from langchain_community.cache import SQLiteCache
    langchain.globals.set_llm_cache(SQLiteCache(database_path="langchain-cache.db"))
    langchain.globals.set_debug(True)

    eval_cfg_file = Path(sys.argv[1])
    print('Loading eval chain from', eval_cfg_file)
    eval_chain = _load_eval_chain_from_cfg(eval_cfg_file)

    for eval_file in sys.argv[2:]:
        print('\n\nEvaluating', eval_file, '\n')
        with langchain_community.callbacks.get_openai_callback() as cb:
            try:
                llm_eval(eval_cfg_file, Path(eval_file), eval_chain)
            finally:
                print(cb)


if __name__ == '__main__':
    main()
