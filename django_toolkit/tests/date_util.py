from django.utils import unittest
from datetime import datetime, date
from django_toolkit.date_util import *

class DateUtilTestCase(unittest.TestCase):

    def test_start_of_month(self):
        self.assertEqual(start_of_month(date(2012, 1, 15)), date(2012, 1, 1))
    
    def test_get_end_of_month(self):
        self.assertEqual(end_of_month(date(2012, 10, 15)), date(2012, 10, 31))

    def test_start_of_previous_month(self):
        self.assertEqual(start_of_month(date(2012, 1, 15), 0, -1), date(2011, 12, 1))

    def test_start_of_next_month(self):
        self.assertEqual(start_of_month(date(2012, 1, 15), 0, 1), date(2012, 2, 1))

class DatePeriodTestCase(unittest.TestCase):
    
    def test_first_of_month(self):
        self.assertEqual(date_period(DATE_FREQUENCY_MONTHLY, 1, date(2012, 12, 1)), (date(2012, 12, 1), date(2012, 12, 31)))
        
    def test_second_of_month(self):
        self.assertEqual(date_period(DATE_FREQUENCY_MONTHLY, 2, date(2012, 2, 2)), (date(2012, 2, 2), date(2012, 3, 1)))
        
    def test_second_of_month_middle_month(self):
        self.assertEqual(date_period(DATE_FREQUENCY_MONTHLY, 2, date(2012, 2, 16)), (date(2012, 2, 2), date(2012, 3, 1)))

    def test_fourth_of_month_middle_month(self):
        self.assertEqual(date_period(DATE_FREQUENCY_MONTHLY, 4, date(2012, 2, 16)), (date(2012, 2, 4), date(2012, 3, 3)))

    def test_twenty_eigth_jan(self):
        self.assertEqual(date_period(DATE_FREQUENCY_MONTHLY, 28, date(2012, 1, 31)), (date(2012, 1, 28), date(2012, 2, 27)))
        
    def test_raises_on_anniversary_greater_than_28th(self):
        self.assertRaises(MaxAnniversaryDayError, date_period, DATE_FREQUENCY_MONTHLY, 29)
        
    def test_raises_on_invalid_frequency(self):
        self.assertRaises(DateFrequencyError, date_period, 'weekly', 1)

    def test_strangeness(self):
        self.assertEqual(date_period(DATE_FREQUENCY_MONTHLY, 15, date(2012, 11, 10)), (date(2012, 10, 15), date(2012, 11, 14)))

class BusinessDaysTestCase(unittest.TestCase):

    def test_business_days_working_week(self):
        self.assertEqual(business_days(date(2012, 11, 12), date(2012, 11, 16)), 5)
        
    def test_business_days_span_weekend(self):
        self.assertEqual(business_days(date(2012, 11, 1), date(2012, 11, 8)), 6)
        
    def test_business_days_entire_month(self):
        self.assertEqual(business_days(date(2012, 11, 1), date(2012, 11, 30)), 22)
        
    def test_business_days_span_months(self):
        self.assertEqual(business_days(date(2012, 11, 1), date(2012, 12, 10)), 28)

    def test_business_days_dates_reversed(self):
        self.assertEqual(business_days(date(2012, 12, 10), date(2012, 11, 1)), 0)
    
    def test_business_days_one_day(self):
        self.assertEqual(business_days(date(2012, 12, 10), date(2012, 12, 10)), 1)
        
    def test_business_days_two_days(self):
        self.assertEqual(business_days(date(2012, 12, 10), date(2012, 12, 11)), 2)

class DaysTestCase(unittest.TestCase):
    
    def test_days_working_week(self):
        self.assertEqual(days(date(2012, 11, 12), date(2012, 11, 16)), 5)
        
    def test_days_span_weekend(self):
        self.assertEqual(days(date(2012, 11, 1), date(2012, 11, 8)), 8)
        
    def test_days_entire_month(self):
        self.assertEqual(days(date(2012, 11, 1), date(2012, 11, 30)), 30)
        
    def test_days_span_months(self):
        self.assertEqual(days(date(2012, 11, 1), date(2012, 12, 10)), 40)

    def test_days_dates_reversed(self):
        self.assertEqual(days(date(2012, 12, 10), date(2012, 11, 1)), 0)
    
    def test_days_one_day(self):
        self.assertEqual(days(date(2012, 12, 10), date(2012, 12, 10)), 1)
        
    def test_days_two_days(self):
        self.assertEqual(days(date(2012, 12, 10), date(2012, 12, 11)), 2)

class DaysInMonthTestCase(unittest.TestCase):
    
    def test_feb_2011(self):
        self.assertEqual(days_in_month(date(2011, 2, 10)), 28)
    
    def test_feb_2012(self):
        self.assertEqual(days_in_month(date(2012, 2, 1)), 29)
    
    def test_oct_2012(self):
        self.assertEqual(days_in_month(date(2012, 10, 31)), 31)
        
class HelperGetAnniversaryPeriodsTestCase(unittest.TestCase):
    
    def test_single_month(self):
        self.assertEqual(
            get_anniversary_periods(date(2012, 11, 1), date(2012, 11, 30)),
            [(date(2012, 11, 1), date(2012, 11, 30))]
        )
    
    def test_across_month(self):
        self.assertEqual(
            get_anniversary_periods(date(2012, 11, 10), date(2012, 12, 9)),
            [
                (date(2012, 11, 10), date(2012, 11, 30)), 
                (date(2012, 12, 1), date(2012, 12, 9))
            ]
        )

    def test_second_day_single_month(self):
        self.assertEqual(
            get_anniversary_periods(date(2012, 11, 2), date(2012, 12, 1), 2),
            [(date(2012, 11, 2), date(2012, 12, 1))]
        )

    def test_second_day_anniversary_across_month(self):
        self.assertEqual(
            get_anniversary_periods(date(2012, 11, 10), date(2012, 12, 9), 2),
            [
                (date(2012, 11, 10), date(2012, 12, 1)), 
                (date(2012, 12, 2), date(2012, 12, 9))
            ]
        )

    def test_fifteen_day_anniversary_across_multiple_months(self):
        self.assertEqual(
            get_anniversary_periods(date(2012, 11, 10), date(2013, 1, 16), 15),
            [
                (date(2012, 11, 10), date(2012, 11, 14)),
                (date(2012, 11, 15), date(2012, 12, 14)),
                (date(2012, 12, 15), date(2013, 1,  14)),
                (date(2013, 1, 15),  date(2013, 1,  16)), 
            ]
        )

    def test_finish_on_anniversary(self):
        self.assertEqual(
            get_anniversary_periods(date(2013, 1, 16), date(2013, 2, 1), 1),
            [
                (date(2013, 1, 16), date(2013, 1, 31)),
                (date(2013, 2, 1), date(2013, 2, 1)),
            ]
        )
        
class DateUtilNextDateTestCase(unittest.TestCase):
    
    def test_start_of_month(self):
        self.assertEqual(
            next_date_for_day(DATE_FREQUENCY_MONTHLY, 1, date(2012, 11, 1)), 
            date(2012, 11, 1)
        )

class DateDayLastWeekTestCase(unittest.TestCase):
    
    def test_monday_last_week_mid_week(self):
        self.assertEqual(
            day_last_week(0, date(2013, 1, 23)), 
            date(2013, 1, 14)
        )
  
    def test_tuesday_last_week(self):
        self.assertEqual(
            day_last_week(1, date(2013, 1, 22)), 
            date(2013, 1, 15)
        )
  
    def test_tuesday_last_week_across_year(self):
        self.assertEqual(
            day_last_week(1, date(2013, 1, 2)), 
            date(2012, 12, 25)
        )

class ExactAnniversariesTestCase(unittest.TestCase):
    
    def test_raises_on_invalid_frequency(self):
        self.assertRaises(DateFrequencyError, exact_anniversaries, 'weekly', 1, date(2012, 3, 1), date(2012, 4, 1))
        
    def test_no_anniversaries_overflow_finish(self):
        self.assertEqual(
            exact_anniversaries(DATE_FREQUENCY_MONTHLY, 1, date(2012, 3, 1), date(2012, 4, 1)),
            False
        )

    def test_no_anniversaries_overflow_start(self):
        self.assertEqual(
            exact_anniversaries(DATE_FREQUENCY_MONTHLY, 4, date(2012, 3, 1), date(2012, 4, 3)),
            False
        )

    def test_one_anniversary_1st_of_month(self):
        self.assertEqual(
            exact_anniversaries(DATE_FREQUENCY_MONTHLY, 1, date(2012, 3, 1), date(2012, 3, 31)),
            1
        )

    def test_one_anniversary_6th_of_month(self):
        self.assertEqual(
            exact_anniversaries(DATE_FREQUENCY_MONTHLY, 6, date(2012, 3, 6), date(2012, 4, 5)),
            1
        )

    def test_two_anniversaries_1st_of_month(self):
        self.assertEqual(
            exact_anniversaries(DATE_FREQUENCY_MONTHLY, 1, date(2012, 3, 1), date(2012, 4, 30)),
            2
        )

    def test_two_anniversaries_16th_of_month(self):
        self.assertEqual(
            exact_anniversaries(DATE_FREQUENCY_MONTHLY, 16, date(2012, 10, 16), date(2012, 12, 15)),
            2
        )

    def test_three_anniversaries_26th_of_month(self):
        self.assertEqual(
            exact_anniversaries(DATE_FREQUENCY_MONTHLY, 26, date(2012, 10, 26), date(2013, 1, 25)),
            3
        )

class QuarterTestCase(unittest.TestCase):
    
    def test_quarter_start_of_quarter(self):
        self.assertEquals(quarter(date(2013, 1, 1)), (date(2013, 1, 1), date(2013, 3, 31)))
        
    def test_quarter_middle_of_quarter(self):
        self.assertEquals(quarter(date(2013, 1, 15)), (date(2013, 1, 1), date(2013, 3, 31)))
        self.assertEquals(quarter(date(2013, 2, 15)), (date(2013, 1, 1), date(2013, 3, 31)))
        self.assertEquals(quarter(date(2013, 3, 15)), (date(2013, 1, 1), date(2013, 3, 31)))

    def test_quarter_end_of_quarter(self):
        self.assertEquals(quarter(date(2013, 3, 31)), (date(2013, 1, 1), date(2013, 3, 31)))
        
class PreviousQuarterTestCase(unittest.TestCase):
    
    def test_previous_quarter_start_of_quarter(self):
        self.assertEquals(previous_quarter(date(2013, 1, 1)), (date(2012, 10, 1), date(2012, 12, 31)))
        
    def test_previous_quarter_middle_of_quarter(self):
        self.assertEquals(previous_quarter(date(2013, 1, 15)), (date(2012, 10, 1), date(2012, 12, 31)))

    def test_previous_quarter_end_of_quarter(self):
        self.assertEquals(previous_quarter(date(2013, 3, 31)), (date(2012, 10, 1), date(2012, 12, 31)))
        