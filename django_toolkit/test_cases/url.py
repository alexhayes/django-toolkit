from django.utils import unittest
from django_toolkit.url import *

class ShortenUrlTestCases(unittest.TestCase):
    
    def test_shorten_url(self):
        url = 'example012345678901234.com.au'
        url = shorten_url(url, 28)
        self.assertEquals(url, 'example01...678901234.com.au')

    def test_does_not_shorten_if_match_length(self):
        self.assertEquals(shorten_url('exampleasdf5678901234.com.au', 32), 'exampleasdf5678901234.com.au')

    def test_does_not_shorten_if_less_length(self):
        self.assertEquals(shorten_url('example.com.au', 32), 'example.com.au')

    def test_large(self):
        self.assertEquals(shorten_url('areallylongsubdomain.areallylongexample.com.au', 16), 'are...ple.com.au')
        
    def test_large_even(self):
        self.assertEquals(shorten_url('areallylongsubdomain.areallylongexamplee.com.au', 16), 'are...lee.com.au')

    def test_large_odd_length(self):
        self.assertEquals(shorten_url('areallylongsubdomain.areallylongexamplee.com.au', 17), 'area...lee.com.au')
        
    def test_tld(self):
        self.assertEquals(shorten_url('areallylongsubdomain.areallylongexamplee.com', 32), 'areallylongsu...longexamplee.com')    
        
    def test_no_tld(self):
        self.assertEquals(shorten_url('areallylongsubdomain.areallylongexampleecom12', 32), 'areallylongsub...gexampleecom12.')
        
    def test_no_www(self):
        self.assertEquals(shorten_url('www.example.com', 16), 'example.com')
        
    def test_www(self):
        self.assertEquals(shorten_url('www.example.com', 16, strip_www=False), 'www.example.com')
        
        
class NetlocNoWwwTestCase(unittest.TestCase):
    
    def test_netloc_no_www(self):
        self.assertEqual(
            netloc_no_www('http://example.com'),
            'example.com'
        )
        self.assertEqual(
            netloc_no_www('http://www.example.com'),
            'example.com'
        )
        self.assertEqual(
            netloc_no_www('http://www.example.com/asdf'),
            'example.com'
        )
        self.assertEqual(
            netloc_no_www('http://wwwjd.example.com/asdf'),
            'wwwjd.example.com'
        )