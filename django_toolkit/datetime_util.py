from datetime import datetime, timedelta
from dateutil import rrule, relativedelta
from django_toolkit.date_util import business_days as dt_business_days
from django_toolkit.date_util import days as dt_days

def start_of_month(dt, d_years=0, d_months=0):
    """
    Given a date, return a date first day of the month.
    
    @param dt: The date to base the return value upon.
    @param d_years: Specify a delta in years to apply to date.
    @param d_months: Specify a delta in months to apply to date.
    
    @see http://code.activestate.com/recipes/476197-first-last-day-of-the-month/
    """
    y, m = dt.year + d_years, dt.month + d_months
    a, m = divmod(m-1, 12)
    return datetime(y+a, m+1, 1)

def end_of_month(dt):
    """
    Given a date, return the last day of the month.
    
    @param dt: The date to base the return value upon.
    """
    return start_of_month(dt, 0, 1) + timedelta(-1)

def business_days(start, stop):
    """
    Return business days between two datetimes (inclusive).
    """
    return dt_business_days(start.date(), stop.date())

def days(start, stop):
    """
    Return days between two datetimes (inclusive).
    """
    return dt_days(start.date(), stop.date())

def quarter(dt):
    """
    Return start/stop datetime for the quarter as defined by dt.
    """
    quarters = rrule.rrule(
       rrule.MONTHLY,
       bymonth = (1, 4, 7, 10),
       bysetpos = -1,
       dtstart = datetime(dt.year, 1, 1),
       count = 8
    )
    first_day = quarters.before(dt, True)
    last_day = quarters.after(dt) - relativedelta.relativedelta(days=1)
    return (first_day, last_day)

def previous_quarter(dt):
    """
    Retrieve the previous quarter for dt
    """
    return quarter( quarter(dt)[0] + timedelta(days=-1) )

