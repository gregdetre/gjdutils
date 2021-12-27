import datetime
import pendulum
from typing import Optional, Union


def dt_str(dt: Optional[datetime.datetime] = None, seconds: bool = True) -> str:
    """
    e.g. 2020-Nov-18 at 7:39:20pm -> '201118_1939_20'
    """
    if dt is None:
        dt = pendulum.now()
    else:
        dt = pendulum.instance(dt)
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


def pendulum_from_date(date: Union[datetime.datetime, datetime.date]) -> datetime.date:
    """
    It's easier to always work with Pendulum objects, so
    convert to that (works from Datetime, Date, or Pendulum).
    """
    return pendulum.date(date.year, date.month, date.day)
