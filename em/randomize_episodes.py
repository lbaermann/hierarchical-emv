from dataclasses import dataclass
from datetime import datetime, timedelta, time
from random import Random
from typing import List, Tuple, Union

import numpy as np

from em.em_tree import HigherLevelSummary
from em.em_util import move_history_to_start_date


@dataclass
class HistoryGenDateTimeSettings:
    rng_base_date: datetime = datetime(year=2024, month=1, day=1, hour=8)
    max_start_date_distance: timedelta = timedelta(days=304)
    allow_before_base_date: bool = True

    skip_day_probability: float = 0.1
    max_skipped_days: int = 3

    min_episodes_per_day: int = 1
    max_episodes_per_day: int = 5
    valid_hours_range: Tuple[int, int] = (8, 20)
    min_distance_between_episodes: timedelta = timedelta(0)

    @classmethod
    def from_dict(cls, d: dict):
        if 'rng_base_date' in d:
            d['rng_base_date'] = datetime(**d['rng_base_date'])
        for field in ['max_start_date_distance', 'min_distance_between_episodes']:
            if field in d:
                d[field] = timedelta(**d[field])
        return cls(**d)


def randomize_datetimes(tmp_episodes: List[HigherLevelSummary],
                        datetime_settings: HistoryGenDateTimeSettings = HistoryGenDateTimeSettings(),
                        rng: Random = None) -> List[HigherLevelSummary]:
    tmp_episodes = list(tmp_episodes)
    if rng is None:
        rng = Random()
    if datetime_settings is None:
        datetime_settings = HistoryGenDateTimeSettings()

    start = gen_random_date(datetime_settings.rng_base_date, datetime_settings.max_start_date_distance, rng,
                            datetime_settings.allow_before_base_date, datetime_settings.valid_hours_range)
    result = []
    while len(tmp_episodes) > 0:
        last_end = result[-1].range[1] if result else start
        num_episodes_next_day = min(rng.randint(datetime_settings.min_episodes_per_day,
                                                datetime_settings.max_episodes_per_day),
                                    len(tmp_episodes))
        next_day = last_end.date() + timedelta(days=1)
        i = 0
        while rng.random() < datetime_settings.skip_day_probability and i < datetime_settings.max_skipped_days:
            next_day = last_end.date() + timedelta(days=1)
            i += 1

        min_hour, max_hour = datetime_settings.valid_hours_range
        # Do not use np.random as it would not use the predefined rng
        hour_floats = np.array([rng.random() for _ in range(num_episodes_next_day)]) * (max_hour - min_hour) + min_hour
        hour_floats.sort()
        minute_floats = (hour_floats % 1) * 60
        second_floats = (minute_floats % 1) * 60
        microseconds = ((second_floats % 1) * 1e6).astype(int)
        for i in range(num_episodes_next_day):
            new_time = time(hour=int(hour_floats[i]),
                            minute=int(minute_floats[i]),
                            second=int(second_floats[i]),
                            microsecond=microseconds[i])
            new_datetime = datetime.combine(next_day, new_time)
            new_datetime = max(new_datetime, last_end + datetime_settings.min_distance_between_episodes)
            result.append(move_history_to_start_date(tmp_episodes.pop(0), new_datetime))
            last_end = result[-1].range[1]

    return result


def gen_random_date(base: datetime, max_delta: timedelta, rng: Random, allow_negative: bool,
                    allowable_hour_range: Tuple[int, int]):
    r = rng.random()
    if allow_negative:
        r = r * 2 - 1
    result = base + r * max_delta

    # Clamp if necessary
    result -= timedelta(hours=max(result.hour - allowable_hour_range[1], 0))
    result += timedelta(hours=max(allowable_hour_range[0] - result.hour, 0))

    return result


def gen_random_date_from_seed(seed: Union[str, int],
                              settings: HistoryGenDateTimeSettings = None):
    rng = Random(seed)
    settings = settings or HistoryGenDateTimeSettings()
    return gen_random_date(settings.rng_base_date, settings.max_start_date_distance, rng,
                           settings.allow_before_base_date, settings.valid_hours_range)
