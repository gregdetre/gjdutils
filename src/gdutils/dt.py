from calendar import monthrange
from datetime import datetime, date, timedelta
import pendulum
from typing import Optional, Union


def dt_str(
    dt: Optional[datetime] = None, seconds: bool = True, tz: Optional[str] = None
) -> str:
    """
    e.g. 2020-Nov-18 at 7:39:20pm -> '201118_1939_20'

    If TZ is None, defaults to UTC. Or set e.g. 'Europe/London'.
    """
    if dt is None:
        dt = pendulum.now(tz=tz)
    else:
        dt = pendulum.instance(dt, tz=tz)
    format = "YYMMDD_HHmm_ss" if seconds else "YYMMDD_HHmm"
    return dt.format(format)


# def dt_str(dt=None, hoursmins=True, seconds=True):
#     """
#     Returns the current date/time as a yymmdd_HHMM_S string,
#     e.g. 091016_1916_21 for 16th Oct, 2009, at 7.16pm in the
#     evening.

#     By default, returns for NOW, unless you feed in DT.
#     """
#     if dt is None:
#         dt = datetime.datetime.now()
#     fmt = "%y%m%d"
#     if hoursmins:
#         fmt += "_%H%M"
#     if seconds:
#         fmt += "_%S"
#     return dt.strftime(fmt)


def str_dt(s):
    """
    Returns the current date/time as a DATETIME object, when
    fed in a YYYYmmdd_HHMM_S string. See DT_STR.
    """
    now = datetime.now()
    try:
        # TODO this was a django function. need to find a replacement
        return now.strptime(s, "%Y%m%d_%H%M_%S")
    except ValueError:
        # without seconds
        try:
            return now.strptime(s, "%Y%m%d_%H%M")
        except ValueError:
            # without time at all
            return now.strptime(s, "%Y%m%d")


def pendulum_from_date(date: Union[datetime, date]) -> date:
    """
    It's easier to always work with Pendulum objects, so
    convert to that (works from Datetime, Date, or Pendulum).
    """
    return pendulum.date(date.year, date.month, date.day)


def timedelta_float(td, units="days"):
    """
    Returns a float of timedelta TD in UNITS
    (either 'days' or 'seconds').

    Can be negative for things in the past.

    timedelta returns the number of
    days and the number of seconds, but you have to combine
    them to get a float timedelta.

    e.g. timedelta_float(now() - dt_last_week) == c. 7.0
    """
    # 86400 = number of seconds in a day
    if units == "days":
        return td.days + td.seconds / 86400.0
    elif units == "seconds":
        return td.days * 86400.0 + td.seconds
    else:
        raise Exception("Unknown units %s" % units)


def serialize_datetimes(d, level=0):
    """
    Recursively walks through a dictionary, serializing datetime objects
    into ISO 8601 formatted strings.

    Set a (somewhat arbitrary) maximum of 20 levels of dictionaries. We
    should never get to more than that, but if we do, it will just stop
    serializing datetimes.
    """
    if level > 20:
        raise ValueError("Too many levels trying to serialize datetimes")

    for k in d.keys():
        if type(d[k]) == datetime:
            d[k] = d[k].isoformat()
        elif type(d[k]) == dict:
            d[k] = serialize_datetimes(d[k], level + 1)
        else:
            pass
    return d


def datetime_to_date(dt):
    return date(year=dt.year, month=dt.month, day=dt.day)


def date_to_datetime(dt):
    if isinstance(dt, datetime):
        return dt
    return datetime(year=dt.year, month=dt.month, day=dt.day)


def month_name(dt):
    return datetime.strftime(dt, "%B")


def near_in_time(dt1, dt2=None):
    """
    Compares two datetime and ensures that they're within 1s
    of each other. Doesn't care which came first. Useful for unit tests.
    """
    if dt2 is None:
        dt2 = datetime.now()
    dt_diff = abs(dt1 - dt2)
    return dt_diff.days == 0 and dt_diff.seconds < 1


def pp_date(dt):
    """
    Human-readable (i.e. pretty-print) dates, e.g. for spreadsheets:

    See http://docs.python.org/tutorial/stdlib.html

    e.g. 31-Oct-2011
    """
    d = date_to_datetime(dt)
    return d.strftime("%d-%b-%Y")


def humanize_minutes(minutes: int):
    """
    e.g.
        humanize_minutes(5) -> '5 minutes'
        humanize_minutes(61) -> '1 hour'
        humanize_minutes(1500) -> 'a day'
    from https://github.com/python-humanize/humanize
    """
    from humanize import naturalday, naturaldelta

    delta = timedelta(minutes=minutes)
    # minimum_unit="minutes" is not supported
    ndelta = naturaldelta(delta)
    return ndelta


def alltime():
    # return YourModel.happened.order_by('dt')[0].dt
    #
    # hardcode to avoid the query
    return datetime(year=2009, month=10, day=31, hour=22, minute=34, second=6)


def first_last_day_of_month(dt):
    """
    Returns two DATETIMES, one for the first and one for the
    last day of the month of DT.
    """
    first_day = datetime(year=dt.year, month=dt.month, day=1)
    nDays = monthrange(dt.year, dt.month)[1]
    last_day = datetime(year=dt.year, month=dt.month, day=nDays)
    return first_day, last_day


def recent_hour(nHours=1, dt=None):
    """
    Returns the DT for 1 hour (i.e. 3600 seconds) ago.
    """
    seconds = nHours * 3600
    dt = dt or datetime.now()
    return dt - timedelta(seconds=seconds)


def recent_day(nDays=1, dt=None):
    """
    Returns the DT for 1 day (i.e. 24 hours) ago.

    If NDAYS == 24 hours * NDAYS.
    """
    dt = dt or datetime.now()
    return dt - timedelta(days=nDays)


def start_of_day(dt=None):
    """
    Returns the Datetime for DT at midnight, i.e. the start of the day.
    """
    dt = dt or datetime.now()
    return datetime(year=dt.year, month=dt.month, day=dt.day)


def end_of_day(dt=None):
    dt = dt or datetime.now()
    return datetime(
        year=dt.year, month=dt.month, day=dt.day, hour=23, minute=59, second=59
    )


def start_of_week(dt=None):
    """
    Returns the DT for the beginning of the week (i.e. the most recent Monday at 00:01.
    """
    # weekday(): Monday = 0. http://docs.python.org/library/datetime.html
    dt = dt or datetime.now()
    # subtract however many days since Monday from today to get to Monday
    return start_of_day(dt - timedelta(days=dt.weekday()))


def end_of_week(dt=None):
    dt = dt or datetime.now()
    return end_of_day(dt + timedelta(days=(6 - dt.weekday())))


def start_of_month(dt=None):
    dt = dt or datetime.now()
    # xxx - we could have also used:
    # start_of_day(now - timedelta(days=now.day))
    return first_last_day_of_month(dt)[0]


def end_of_month(dt=None):
    dt = dt or datetime.now()
    return first_last_day_of_month(dt)[1] + timedelta(hours=23, minutes=59, seconds=59)


def day_containing(dt=None):
    """Return the half-open day interval containing dt.

    i.e. if dt is Today 12:26, return (Today 00:00, Tomorrow 00:00).
    This can be used for a half-open comparison:

        p, n = day_containing()
        if x >= p and x < n:
            # Do something because x is today.
    """

    p = start_of_day(dt)
    n = p + timedelta(days=1)

    return p, n


def daily_iter(start, end):
    """Iterate over half-open day intervals pairwise until the end of the range falls after end."""

    p = start
    n = start + timedelta(days=1)

    while n < end:
        yield p, n
        p = n
        n = n + timedelta(days=1)


def week_containing(dt=None):
    """Returns a half-open interval of the week containing dt, starting on Sunday."""

    p = start_of_week(dt)
    n = p + timedelta(days=7)
    return p, n


def weekly_iter(start, end):
    """Iterate over weeks pairwise until the end of the range falls after end."""

    p = start
    n = start + timedelta(days=7)

    while n < end:
        yield p, n
        p = n
        n = n + timedelta(days=7)


def date_from_datetime(d: date, as_pendulum: bool = False):
    if as_pendulum:
        return pendulum.date(d.year, d.month, d.day)
    else:
        return datetime(d.year, d.month, d.day, hour=0, minute=0)
