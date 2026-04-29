from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Union, Optional, Any, List

import PIL.Image
import cv2
from langchain.output_parsers import OutputFixingParser
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.outputs import Generation
from langchain_core.prompts import PromptTemplate

from em.em_tree import HigherLevelSummary, GoalBasedSummary, EventBasedSummary


def move_history_to_start_date(history: HigherLevelSummary, start_date: datetime) -> HigherLevelSummary:
    old_start = history.range[0]
    diff = start_date - old_start

    def _deep_adjust(h: Union[HigherLevelSummary, GoalBasedSummary, EventBasedSummary]):
        if isinstance(h, EventBasedSummary):
            for s in h.scenes:
                s.raw.timestamp += diff
        elif isinstance(h, GoalBasedSummary):
            for e in h.events:
                _deep_adjust(e)
        else:
            for c in h.children:
                _deep_adjust(c)

    history = deepcopy(history)
    _deep_adjust(history)

    return history


class LazyLoadPILImage:

    def __init__(self, path: Union[str, Path]):
        super().__init__()
        self._path = str(path)
        self._loaded_img = None

    def __repr__(self):
        return '<PIL.Image.Image ...>'

    def __getattribute__(self, __name):
        if ('__' in __name or __name.startswith('_') or __name in dir(self)) and __name != '__array_interface__':
            return super().__getattribute__(__name)
        if self._loaded_img is None:
            self._loaded_img = self._load_img()
        return getattr(self._loaded_img, __name)

    def _load_img(self):
        return PIL.Image.open(self._path)

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['_loaded_img']  # Don't pickle loaded img
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self._loaded_img = None


class LazyVideoFramePILImage(LazyLoadPILImage):

    def __init__(self, video_path: Union[str, Path], *,
                 frame_num: Optional[int] = None,
                 frame_second: Optional[float] = None):
        super().__init__(video_path)
        assert frame_num is not None or frame_second is not None, 'One of frame_num and frame_second is required'
        assert frame_num is None or frame_second is None, 'Do not specify both frame_num and frame_second'
        self._frame_timestamp = frame_second
        self._frame_num = frame_num

    def _load_img(self):
        video = cv2.VideoCapture(str(self._path))
        if self._frame_num is None:
            video.set(cv2.CAP_PROP_POS_MSEC, self._frame_timestamp * 1000)
        else:
            video.set(cv2.CAP_PROP_POS_FRAMES, self._frame_num)
        success, image = video.read()
        if not success:
            raise IOError(
                f'Cannot read frame {f"at {self._frame_timestamp}s" if self._frame_num is None else self._frame_num}'
                f' from {self._path}')
        color_converted = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return PIL.Image.fromarray(color_converted)


class _InitialTextForgivingJsonOutputParser(JsonOutputParser):
    json_keyword: str = 'JSON:'

    def parse_result(self, result: List[Generation], *, partial: bool = False) -> Any:
        text = result[0].text
        text = text.strip()
        start_idx = text.find(self.json_keyword)
        if start_idx > -1:
            text = text[start_idx + len(self.json_keyword):]
        return super().parse_result([Generation(text=text)], partial=partial)


_FIX_JSON_PROMPT = PromptTemplate.from_template("""
This output is not a valid JSON object.
--------------
{completion}
--------------
Error: {error}

Fix the error. Respond with only a copy of the above JSON object, with errors fixed. 
No other output except valid JSON:""".strip())


def json_fixing_parser(llm):
    return OutputFixingParser.from_llm(llm=llm, parser=JsonOutputParser(), prompt=_FIX_JSON_PROMPT)


def initial_text_forgiving_json_fixing_parser(llm, json_keyword='JSON:'):
    return OutputFixingParser.from_llm(llm=llm, prompt=_FIX_JSON_PROMPT,
                                       parser=_InitialTextForgivingJsonOutputParser(json_keyword=json_keyword))
