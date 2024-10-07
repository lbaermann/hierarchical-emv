import argparse
import ast
import pickle
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Union

from langchain_core.language_models import BaseChatModel

from em.ego4d.ego4d import load_history_from_video_recap_pickle
from em.em_util import move_history_to_start_date
from lmp.setup import instantiate_llm


def load_and_enrich_history_from_video_recap(pickle_history_file: Path,
                                             obj_proposal_llm: BaseChatModel,
                                             convert_to_first_person_llm=None,
                                             start_time: datetime = None,
                                             yolo_world: Union['YoloWorld', dict] = None,
                                             clip_selector: Union['ClipBasedObjectCategoryProposal', dict] = None,
                                             **insert_objs_kwargs):
    if convert_to_first_person_llm is None:
        enriched_file = pickle_history_file.with_suffix('.objs.pkl')
    else:
        enriched_file = pickle_history_file.with_suffix('.first_person.objs.pkl')

    if enriched_file.is_file():
        history = pickle.loads(enriched_file.read_bytes())
    else:
        from ..insert_objs_socratic import insert_objs_into_history, YoloWorld, ClipBasedObjectCategoryProposal
        history = load_history_from_video_recap_pickle(pickle_history_file, convert_to_first_person_llm, start_time)
        history = insert_objs_into_history(
            history, obj_proposal_llm,
            YoloWorld(**yolo_world) if isinstance(yolo_world, dict) else yolo_world,
            ClipBasedObjectCategoryProposal(**clip_selector) if isinstance(clip_selector, dict) else clip_selector,
            **insert_objs_kwargs)
        enriched_file.write_bytes(pickle.dumps(history))

    if start_time is not None:
        history = move_history_to_start_date(history, start_time)
    return history


def main():
    from langchain_community.cache import SQLiteCache
    import langchain.globals
    langchain.globals.set_llm_cache(SQLiteCache(database_path="langchain-cache.db"))
    langchain.globals.set_verbose(True)

    parser = argparse.ArgumentParser()
    parser.add_argument('--llm', type=ast.literal_eval, default=None,
                        help='Sets both obj-proposal-llm and convert-to-first-person-llm')
    parser.add_argument('--obj-proposal-llm', type=ast.literal_eval, default=None)
    parser.add_argument('--convert-to-first-person-llm', type=ast.literal_eval, default=None)
    parser.add_argument('--yolo-world-cfg', type=ast.literal_eval, required=True)
    parser.add_argument('--clip-selector-cfg', type=ast.literal_eval, default={})
    parser.add_argument('--insert-objs-cfg', type=ast.literal_eval, default={})
    parser.add_argument('history_pickle_files', nargs='+', type=Path)

    args = parser.parse_args()
    assert args.llm or args.obj_proposal_llm

    if args.obj_proposal_llm is None:
        args.obj_proposal_llm = deepcopy(args.llm)
    if args.llm and args.convert_to_first_person_llm is None:
        args.convert_to_first_person_llm = deepcopy(args.llm)

    obj_proposal_llm = instantiate_llm(args.obj_proposal_llm)
    convert_to_first_person_llm = (None if args.convert_to_first_person_llm is None
                                   else instantiate_llm(args.convert_to_first_person_llm))

    from em.insert_objs_socratic import YoloWorld, ClipBasedObjectCategoryProposal
    yolo_world = YoloWorld(**args.yolo_world_cfg)
    clip_selector = ClipBasedObjectCategoryProposal(**args.clip_selector_cfg)

    for history_pickle in args.history_pickle_files:
        print(history_pickle.stem)
        # noinspection PyTypeChecker
        load_and_enrich_history_from_video_recap(
            history_pickle,
            obj_proposal_llm,
            convert_to_first_person_llm,
            yolo_world=yolo_world,
            clip_selector=clip_selector,
            **args.insert_objs_cfg
        )


if __name__ == '__main__':
    main()
