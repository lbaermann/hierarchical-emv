import ast
import json
import sys
from pathlib import Path

import langchain.globals
from langchain_community.cache import SQLiteCache

from em.ego4d import load_history_from_narrations
from em.llm_summary import LLMBasedSummarizer
from em.randomize_episodes import gen_random_date_from_seed
from lmp.setup import instantiate_llm


def create_summary_samples_from_hcap(ego4d_base_dir: Path,
                                     output_dir: Path,
                                     num_samples=10,
                                     convert_to_first_person_llm=None):
    hcap_dir = ego4d_base_dir.parent / 'Ego4D-HCap'
    assert hcap_dir.is_dir(), str(hcap_dir.absolute())
    hcap_train = json.loads((hcap_dir / 'videos_train.json').read_text())
    hcap_train.sort(key=lambda x: x['vid'])  # For reproducibility
    produced_samples = 0
    while produced_samples < num_samples and hcap_train:
        annotation = hcap_train.pop(0)
        video_id = annotation['vid']
        if 'narration_pass' not in annotation:
            continue
        narration_pass = annotation['narration_pass'][-1:]
        input_file = output_dir / f'{video_id}_{narration_pass}.input'
        if input_file.exists():  # Sometimes, the dataset contains redundant annotations. Choose only the first one.
            continue

        history = load_history_from_narrations(ego4d_base_dir, video_id, convert_to_first_person_llm,
                                               gen_random_date_from_seed(video_id), narration_pass)

        goals = LLMBasedSummarizer.format_context(history.children)
        input_file.write_text(goals)

        top_level_summary = {f'0-{len(history.children)}': history.nl_summary}
        (output_dir / f'{video_id}_{narration_pass}.output').write_text(json.dumps(top_level_summary, indent=2))
        produced_samples += 1


if __name__ == '__main__':
    langchain.globals.set_llm_cache(SQLiteCache(database_path="langchain-cache.db"))
    langchain.globals.set_verbose(True)

    create_summary_samples_from_hcap(
        Path(sys.argv[1]).absolute(),
        Path(__file__).parent,
        convert_to_first_person_llm=instantiate_llm(ast.literal_eval(sys.argv[2])) if len(sys.argv) > 2 else None,
        num_samples=int(sys.argv[3]) if len(sys.argv) > 3 else 10,
    )
