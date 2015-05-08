from django.utils import unittest
from datetime import datetime, date
from django_toolkit.datetime_util import *

class DateTimeUtilTestCase(unittest.TestCase):

    def test_start_of_month(self):
        first_day = datetime(2012, 1, 1)
        self.assertEqual(start_of_month(datetime(2012, 1, 15)), first_day)
    
    def test_get_end_of_month(self):
        last_day = datetime(2012, 10, 31)
        self.assertEqual(end_of_month(datetime(2012, 10, 15)), last_day)

    def test_start_of_previous_month(self):
        self.assertEqual(start_of_month(datetime(2012, 1, 15), 0, -1), datetime(2011, 12, 1))

    def test_start_of_next_month(self):
        self.assertEqual(start_of_month(datetime(2012, 1, 15), 0, 1), datetime(2012, 2, 1))

class BusinessDaysTestCase(unittest.TestCase):

    def test_business_days_accepts_datetime(self):
        """
        Test that datetime_business_days accepts datetime - all other testing occurs in DateUtilTestCase.
        """
        self.assertEqual(business_days(datetime(2012, 11, 12), datetime(2012, 11, 16)), 5)
        
class QuarterTestCase(unittest.TestCase):
    
    def test_quarter_start_of_quarter(self):
        self.assertEquals(quarter(datetime(2013, 1, 1)), (datetime(2013, 1, 1), datetime(2013, 3, 31)))
        
    def test_quarter_middle_of_quarter(self):
        self.assertEquals(quarter(datetime(2013, 1, 15)), (datetime(2013, 1, 1), datetime(2013, 3, 31)))
        self.assertEquals(quarter(datetime(2013, 2, 15)), (datetime(2013, 1, 1), datetime(2013, 3, 31)))
        self.assertEquals(quarter(datetime(2013, 3, 15)), (datetime(2013, 1, 1), datetime(2013, 3, 31)))

    def test_quarter_end_of_quarter(self):
        self.assertEquals(quarter(datetime(2013, 3, 31)), (datetime(2013, 1, 1), datetime(2013, 3, 31)))
        
class PreviousQuarterTestCase(unittest.TestCase):
    
    def test_previous_quarter_start_of_quarter(self):
        self.assertEquals(previous_quarter(datetime(2013, 1, 1)), (datetime(2012, 10, 1), datetime(2012, 12, 31)))
        
    def test_previous_quarter_middle_of_quarter(self):
        self.assertEquals(previous_quarter(datetime(2013, 1, 15)), (datetime(2012, 10, 1), datetime(2012, 12, 31)))

    def test_previous_quarter_end_of_quarter(self):
        self.assertEquals(previous_quarter(datetime(2013, 3, 31)), (datetime(2012, 10, 1), datetime(2012, 12, 31)))
        