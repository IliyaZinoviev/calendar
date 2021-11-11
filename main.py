from datetime import date

from calendar import rest_day_count, Calendar, get_calendar, print_calendar

if __name__ == '__main__':
    start: date = date(2021, 11, 26)
    end: date = date(2022, 9, 19)
    days: int = rest_day_count(start, end)
    res: Calendar = get_calendar(start, days, 46, True, 7)
    print_calendar(res)
