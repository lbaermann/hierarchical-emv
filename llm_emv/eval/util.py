import subprocess
from datetime import timedelta
from pathlib import Path
from random import Random

from em.em_tree import HigherLevelSummary
from em.llm_summary import LLMBasedSummarizer
from em.randomize_episodes import HistoryGenDateTimeSettings, gen_random_date
from lmp.setup import instantiate_llm


def make_llm_summarizer_from_cfg(cfg: dict):
    cfg = dict(cfg)
    cfg.setdefault('llm', {'type': 'ChatOpenAI', 'model_name': 'gpt-4o'})
    # noinspection PyTypeChecker
    return LLMBasedSummarizer(instantiate_llm(cfg.pop('llm')), **cfg)


def pick_random_question_date_after_history(history: HigherLevelSummary,
                                            rng: Random,
                                            datetime_settings: HistoryGenDateTimeSettings = None):
    if datetime_settings is None:
        datetime_settings = HistoryGenDateTimeSettings()
    num_skipped_days = 0
    while (rng.random() < datetime_settings.skip_day_probability
           and num_skipped_days < datetime_settings.max_skipped_days):
        num_skipped_days += 1
    base = history.range[1]
    if base.hour > datetime_settings.valid_hours_range[1]:
        base = base.replace(day=base.day + 1,
                            hour=datetime_settings.valid_hours_range[0],
                            minute=0, second=0, microsecond=0)
        difference_to_end_of_range = timedelta(
            hours=datetime_settings.valid_hours_range[1] - datetime_settings.valid_hours_range[0])
    else:
        end_of_range_on_same_day = base.replace(hour=datetime_settings.valid_hours_range[1],
                                                minute=0, second=0, microsecond=0)
        difference_to_end_of_range = end_of_range_on_same_day - base
    return gen_random_date(
        base=base,
        max_delta=timedelta(days=num_skipped_days) + difference_to_end_of_range,
        rng=rng,
        allow_negative=False,
        allowable_hour_range=datetime_settings.valid_hours_range
    )


def determine_git_commit():
    return subprocess.run(['git', 'rev-parse', 'HEAD'],
                          cwd=Path(__file__).parent,
                          stdout=subprocess.PIPE,
                          text=True).stdout.strip()
