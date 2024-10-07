# Imported from
# https://gitlab.com/lbaermann/verbalization-of-episodic-memory/-/blob/master/em_verbalization_net/data_generator
from datetime import datetime, timedelta


class Grammar:

    def __or__(self, other):
        return Or(self, convert_to_grammar(other))

    def __ror__(self, other):
        return Or(convert_to_grammar(other), self)

    def __add__(self, other):
        return Concat(self, convert_to_grammar(other))

    def __radd__(self, other):
        return convert_to_grammar(other) + self

    def generate_all(self):
        raise NotImplementedError

    def draw_sample(self, random):
        raise NotImplementedError

    def list_subtypes(self) -> set:
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError


def convert_to_grammar(obj):
    if isinstance(obj, str):
        obj = Terminal(obj)
    return obj


def optional(expr):
    expr = convert_to_grammar(expr)
    return expr | ""


class Terminal(Grammar):

    def __init__(self, content: str):
        super().__init__()
        assert isinstance(content, str), f'{content} :: {type(content)}'
        self.content = content

    def __str__(self):
        return self.content

    def generate_all(self):
        yield self.content

    def draw_sample(self, random):
        return self.content

    def list_subtypes(self) -> set:
        return {Terminal}

    def __len__(self):
        return 1


class Concat(Grammar):

    def __init__(self, first: Grammar, second: Grammar):
        super().__init__()
        assert isinstance(first, Grammar)
        assert isinstance(second, Grammar)
        self.first = first
        self.second = second

    def __str__(self):
        return str(self.first) + str(self.second)

    def generate_all(self):
        for a in self.first.generate_all():
            for b in self.second.generate_all():
                yield a + b

    def draw_sample(self, random):
        a = self.first.draw_sample(random)
        b = self.second.draw_sample(random)
        return a + b

    def list_subtypes(self) -> set:
        return self.first.list_subtypes().union(self.second.list_subtypes()).union({Concat})

    def __len__(self):
        return len(self.first) * len(self.second)


class Or(Grammar):

    def __init__(self, first: Grammar, second: Grammar):
        super().__init__()
        assert isinstance(first, Grammar)
        assert isinstance(second, Grammar)
        self.first = first
        self.second = second

    def __str__(self):
        return "(" + str(self.first) + "|" + str(self.second) + ")"

    def generate_all(self):
        yield from self.first.generate_all()
        yield from self.second.generate_all()

    def draw_sample(self, random):
        # Need to normalize a large Or of Ors so that each option has equal probability!
        options = self._get_non_or_children()
        choice = random.choices(options, weights=[len(o) for o in options], k=1)[0]
        return choice.draw_sample(random)

    def _get_non_or_children(self):
        non_or_children = []
        if isinstance(self.first, Or):
            non_or_children += self.first._get_non_or_children()
        else:
            non_or_children.append(self.first)
        if isinstance(self.second, Or):
            non_or_children += self.second._get_non_or_children()
        else:
            non_or_children.append(self.second)
        return non_or_children

    def list_subtypes(self) -> set:
        return self.first.list_subtypes().union(self.second.list_subtypes()).union({Or})

    def __len__(self):
        return len(self.first) + len(self.second)


lf = "\n"
T = Terminal
o = optional

int_to_string_dict = {
    1: 'one',
    2: 'two',
    3: 'three',
    4: 'four',
    5: 'five',
    6: 'six',
    7: 'seven',
    8: 'eight',
    9: 'nine',
    10: 'ten',
    11: 'eleven',
    12: 'twelve',
}


def int_to_string(i: int):
    if i in int_to_string_dict:
        return int_to_string_dict[i]
    else:
        return str(i)


def hour_to_daytime(hour: int):
    if hour < 10:
        return 'in the morning'
    elif hour < 12:
        return 'before noon'
    elif hour < 14:
        return 'at noon'
    elif hour < 18:
        return 'in the afternoon'
    else:
        return 'in the evening'


def get_time_ref(ref: datetime, now: datetime, prefer_exact=False):
    abs_day = (T(ref.strftime('on %b %d'))
               | ref.strftime('on %B %d'))
    diff_to_full_hour = -ref.minute if ref.minute < 30 else 60 - ref.minute
    ref_rounded = ref + timedelta(minutes=diff_to_full_hour)
    abs_hour = (T(ref.strftime('%H:%M'))
                # | ref.strftime('%I:%M %p')
                )
    if prefer_exact:
        abs_hour |= T(ref.strftime('%H:%M:%S'))
    else:
        abs_hour |= o('about ') + (T(ref_rounded.strftime('%H o clock'))
                                   | ref_rounded.strftime('%I %p'))
        if ref_rounded.hour < 10:
            # Without trailing 0
            abs_hour |= o('about ') + str(ref_rounded.hour) + ' o clock'
    absolute = abs_day + ' at ' + abs_hour

    delta = now - ref
    delta_minutes = round(delta.seconds / 60)
    delta_hours = round(delta_minutes / 60)
    timespec = (T('at ') + abs_hour)
    if not prefer_exact:
        timespec |= hour_to_daytime(ref.hour)
    if delta.days == 0 and delta_hours <= now.hour:
        rel = o('today ') + timespec
        if delta_hours > 1:
            # rel |= o('about ') + int_to_string(delta_hours) + ' hours ago'
            if not prefer_exact:
                rel |= 'in the last ' + int_to_string(delta_minutes // 60 + 1) + ' hours'
        elif delta_hours == 1:
            # rel |= o('about ') + 'one hour ago'
            if not prefer_exact:
                rel |= 'in the last hour'
        else:
            rel |= int_to_string(delta_minutes) + ' minutes ago'
            if not prefer_exact:
                rel |= 'about ' + int_to_string(round(delta_minutes / 5) * 5) + ' minutes ago'
            # rel |= (T('in') | 'during') + ' the last hour'
    elif (delta.days == 1 and delta_hours <= now.hour) or (delta.days == 0 and delta_hours > now.hour):
        rel = T('yesterday ') + timespec
    else:
        rel = T(int_to_string(delta.days + (delta_hours > now.hour))) + ' days ago ' + timespec

    return rel | absolute

