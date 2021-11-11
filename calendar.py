from datetime import date, timedelta
from enum import Enum
from typing import NamedTuple, TypeAlias

from int_dist_gen import IntDistGenFactory


class IntervalType(str, Enum):
    FREEZE = 'выходн'
    WORKOUT = 'рабоч'


class CalendarItem(NamedTuple):
    start: date
    end: date
    interval_type: IntervalType
    count: int


Calendar: TypeAlias = [CalendarItem]


def get_calendar(
        start_date: date, workout_days: int, freeze_days: int, is_workout_interval: bool, min_freeze_interval: int
) -> Calendar:
    freeze_interval_count = freeze_days // min_freeze_interval
    rest_freeze_days = freeze_days % min_freeze_interval
    if is_workout_interval:
        workout_interval_count = freeze_interval_count + 1
    else:
        workout_interval_count = freeze_interval_count
    min_workout_interval = workout_days // workout_interval_count
    rest_workout_days = workout_days % workout_interval_count
    rest_freeze_days_dist_gen = IntDistGenFactory.get_int_dist_gen(rest_freeze_days, freeze_interval_count)
    rest_workout_days_dist_gen = IntDistGenFactory.get_int_dist_gen(rest_workout_days, workout_interval_count)
    curr_interval: int
    curr_interval_type: IntervalType
    result: Calendar = []
    while workout_days > 0:
        if is_workout_interval:
            curr_interval = min_workout_interval + next(rest_workout_days_dist_gen)
            curr_interval_type = IntervalType.WORKOUT
            workout_days -= curr_interval
        else:
            curr_interval = min_freeze_interval + next(rest_freeze_days_dist_gen)
            curr_interval_type = IntervalType.FREEZE
        start = start_date
        start_date += timedelta(days=curr_interval)
        end = start_date - timedelta(days=1)
        result.append(CalendarItem(start, end, curr_interval_type, curr_interval))
        is_workout_interval = not is_workout_interval
    return tuple(result)


def print_calendar(calendar: Calendar):
    for item in calendar:
        count = item.count
        res = f'{item.start.isoformat()} - {item.end.isoformat()} - {count} {item.interval_type}'
        remainder = count % 10
        if count != 11 and remainder == 1:
            if item.interval_type == item.interval_type.WORKOUT:
                res += 'ий'
            else:
                res += 'ой'
        else:
            if item.interval_type == item.interval_type.WORKOUT:
                res += 'их'
            else:
                res += 'ых'
        res += ' '
        if count != 11 and remainder == 1:
            res += 'день'
        elif 11 > count > 15 and 1 > remainder < 5:
            res += 'дня'
        else:
            res += 'дней'
        print(res)


def rest_day_count(start: date, end: date) -> int:
    return (end - start).days
