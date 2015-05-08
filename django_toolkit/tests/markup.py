from django.utils import unittest
from django_toolkit.markup.html import get_anchor_href, get_anchor_contents


class HtmlGetAnchorHrefTestCase(unittest.TestCase):

    def test_finds_single_href(self):
        self.assertEquals(
            get_anchor_href('<a href="http://example.com">Test</a>'),
            [u'http://example.com']
        )

    def test_finds_two_hrefs(self):
        self.assertEquals(
            get_anchor_href('<a href="http://example.com">Test</a><a href="http://example2.com">Test 2</a>'),
            [u'http://example.com', u'http://example2.com']
        )

    def test_finds_two_duplicates(self):
        self.assertEquals(
            get_anchor_href('<a href="http://example.com">Test</a><a href="http://example.com">Test 2</a>'),
            [u'http://example.com', u'http://example.com']
        )

    def test_finds_hrefs_inside_otherstuff(self):
        self.assertEquals(
            get_anchor_href('Here is a <a href="http://example.com/?blah=1234&something-else=KKdjfkdksa">link</a> to somewhere...'),
            [u'http://example.com/?blah=1234&something-else=KKdjfkdksa']
        )


class HtmlGetAnchorHtmlTestCase(unittest.TestCase):

    def test_finds_single_href(self):
        self.assertEquals(
            get_anchor_contents('<a href="http://example.com">Test</a>'),
            [u'Test']
        )

    def test_finds_two_hrefs(self):
        self.assertEquals(
            get_anchor_contents('<a href="http://example.com">Test</a><a href="http://example2.com">Test 2</a>'),
            [u'Test', u'Test 2']
        )

    def test_finds_two_duplicates(self):
        self.assertEquals(
            get_anchor_contents('<a href="http://example.com">Test</a><a href="http://example.com">Test</a>'),
            [u'Test', u'Test']
        )

    def test_finds_hrefs_inside_otherstuff(self):
        self.assertEquals(
            get_anchor_contents('Here is a <a href="http://example.com/?blah=1234&something-else=KKdjfkdksa">link</a> to somewhere...'),
            [u'link']
        )
