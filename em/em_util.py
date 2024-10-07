from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Union, Optional

import PIL.Image
import cv2

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
            raise IOError(f'Cannot read frame {self._frame_num} from {self._path}')
        color_converted = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return PIL.Image.fromarray(color_converted)
