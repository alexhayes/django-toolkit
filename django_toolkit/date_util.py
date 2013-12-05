from datetime import date, timedelta, datetime
from dateutil import rrule
from calendar import monthrange
from dateutil.relativedelta import relativedelta

DATE_FREQUENCY_MONTHLY = 'monthly'

class DateFrequencyError(Exception): pass
class MaxAnniversaryDayError(Exception): pass

def start_of_month(d, d_years=0, d_months=0):
    """
    Given a date, return a date first day of the month.
    
    @param d: The date to base the return value upon.
    @param d_years: Specify a delta in years to apply to date.
    @param d_months: Specify a delta in months to apply to date.
    
    @see http://code.activestate.com/recipes/476197-first-last-day-of-the-month/
    """
    y, m = d.year + d_years, d.month + d_months
    a, m = divmod(m-1, 12)
    return date(y+a, m+1, 1)

def end_of_month(d):
    """
    Given a date, return the last day of the month.
    
    @param d: The date to base the return value upon.
    """
    return start_of_month(d, 0, 1) + timedelta(-1)

def business_days(start, stop):
    """
    Return business days between two inclusive dates - ignoring public holidays.
    
    Note that start must be less than stop or else 0 is returned.
    
    @param start: Start date
    @param stop: Stop date
    @return int
    """
    dates=rrule.rruleset()
    # Get dates between start/stop (which are inclusive)
    dates.rrule(rrule.rrule(rrule.DAILY, dtstart=start, until=stop))
    # Exclude Sat/Sun 
    dates.exrule(rrule.rrule(rrule.DAILY, byweekday=(rrule.SA, rrule.SU), dtstart=start)) 
    return dates.count()

def days(start, stop):
    """
    Return days between start & stop (inclusive)
    
    Note that start must be less than stop or else 0 is returned.
    
    @param start: Start date
    @param stop: Stop date
    @return int
    """
    dates=rrule.rruleset()
    # Get dates between start/stop (which are inclusive)
    dates.rrule(rrule.rrule(rrule.DAILY, dtstart=start, until=stop))
    return dates.count()

def days_in_month(dt):
    return monthrange(dt.year, dt.month)[1]

def get_anniversary_periods(start, finish, anniversary=1):
    """
    Return a list of anniversaries periods between start and finish. 
    """
    import sys
    current = start
    periods = []
    while current <= finish:
        (period_start, period_finish) = date_period(DATE_FREQUENCY_MONTHLY, anniversary, current)
        current = period_start + relativedelta(months=+1)
        period_start = period_start if period_start > start else start
        period_finish = period_finish if period_finish < finish else finish
        periods.append((period_start, period_finish))
    return periods

def date_period(frequency, anniversary, now=None):
    """
    Retrieve a date period given a day of month.
    
    For example, if the period is month:15 and now is equal
    to 2012-11-22 then this method will return the following:
    
        (date(2012, 11, 15), date(2012, 12, 14)) 
    
    Other examples:
        monthly:1 with now 2012-12-1 would return: (date(2012, 11, 1), date(2012, 12, 1))
    
    @param now: A date used to determine some point within a date period.
    @return tuple with date start and stop dates.
    @raise MaxAnniversaryDayError
    @raise DateFrequencyError
    """
    if frequency != DATE_FREQUENCY_MONTHLY:
        raise DateFrequencyError("Only monthly date frequency is supported - not '%s'" % (frequency))
    
    if anniversary > 28:
        raise MaxAnniversaryDayError("'%s' is greater than maximum allowed anniversary day 28." % anniversary)
    
    if not now:
        now = date.now()
   
    if now.day >= anniversary:
        start = date(now.year, now.month, anniversary)
        stop = start + relativedelta(months=+1) + relativedelta(days=-1)
    else:
        stop = date(now.year, now.month, anniversary)
        start = stop + relativedelta(months=-1)
        stop = stop  + relativedelta(days=-1)
    return (start, stop,)
    
def next_date_period (frequency, day, now=None):
    start = next_date_for_day(frequency, day, now)
    stop = start + relativedelta(months=+1)
    return (start, stop,)
     
def next_date_for_day(frequency, day, now=None):
    if frequency != DATE_FREQUENCY_MONTHLY:
        raise DateFrequencyError("Only monthly date frequency is supported - not '%s'" % (frequency))

    if not now:
        now = date.now()
    
    if now.day == day:
        return now

    return date_period(frequency, day, now)[1]

def day_last_week(day, now=False):
    if not now:
        now = date.today()
    return now - timedelta(days=now.weekday()) + timedelta(days=day, weeks=-1)

def exact_anniversaries(frequency, anniversary, start, finish):
    """
    Returns the number of exact anniversaries if start and finish represent an anniversary.
    
    ie.. 
    
    exact_anniversaries(DATE_FREQUENCY_MONTHLY, 10, date(2012, 2, 10), date(2012, 3, 9)) returns 1
    exact_anniversaries(DATE_FREQUENCY_MONTHLY, 10, date(2012, 2, 10), date(2012, 4, 9)) returns 2
    """
    if frequency != DATE_FREQUENCY_MONTHLY:
        raise DateFrequencyError("Only monthly date frequency is supported - not '%s'" % (frequency))
    
    if start.day != anniversary:
        return False

    periods = 0
    current = start
    while current <= finish:
        period_end = current + relativedelta(months=+1, days=-1)
        if period_end <= finish:
            periods += 1
        else:
            return False
        current = current + relativedelta(months=+1)
    return periods

def quarter(d):
    """
    Return start/stop datetime for the quarter as defined by dt.
    """
    from django_toolkit.datetime_util import quarter as datetime_quarter
    first_date, last_date = datetime_quarter(datetime(d.year, d.month, d.day))
    return first_date.date(), last_date.date()

def previous_quarter(d):
    """
    Retrieve the previous quarter for dt
    """
    from django_toolkit.datetime_util import quarter as datetime_quarter
    return quarter( (datetime_quarter(datetime(d.year, d.month, d.day))[0] + timedelta(days=-1)).date() )