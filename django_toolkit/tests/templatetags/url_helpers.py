from django.utils import unittest
from django_toolkit.tests.url.shorten import ShortenUrlTestCase, \
    NetlocNoWwwTestCase
from django_toolkit.templatetags.url_helpers import shorten_url, netloc_no_www


class ShortenUrlTemplateTagTestCases(ShortenUrlTestCase):

    @property
    def shorten_url(self):
        return shorten_url


class NetlocNoWwwTemplateTagTestCase(NetlocNoWwwTestCase):

    @property
    def netloc_no_www(self):
        return netloc_no_www
