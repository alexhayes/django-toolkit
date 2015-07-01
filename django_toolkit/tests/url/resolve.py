from django.utils import unittest
from django_toolkit.url.resolve import url_with_protocol, resolve_url, \
    DESKTOP_USER_AGENT, MOBILE_USER_AGENT
from httmock import all_requests, HTTMock, response


@all_requests
def response_content(url, request):
    if request.headers['User-Agent'] == DESKTOP_USER_AGENT:
        request.url = 'http://example.com/'
        return {'status_code': 200}
    elif request.headers['User-Agent'] == MOBILE_USER_AGENT:
        request.url = 'http://m.example.com/'
        return {'status_code': 200}


class UrlWithProtocolTestCases(unittest.TestCase):

    def test_url_with_protocol(self):
        url = 'example.com'
        url = url_with_protocol(url)
        self.assertEquals(url, 'http://example.com')

    def test_url_with_protocol_www(self):
        url = 'www.example.com'
        url = url_with_protocol(url)
        self.assertEquals(url, 'http://www.example.com')

    def test_url_with_protocol_http(self):
        url = 'http://www.example.com'
        url = url_with_protocol(url)
        self.assertEquals(url, 'http://www.example.com')

    def test_url_with_protocol_path(self):
        url = 'example.com/path.html'
        url = url_with_protocol(url)
        self.assertEquals(url, 'http://example.com/path.html')


class ResolveUrlTestCases(unittest.TestCase):

    def test_resolve_url(self):
        with HTTMock(response_content):
            url = 'exampledfasdaf.com'
            urls = resolve_url(url)
            self.assertEquals(len(urls), 2)
            self.assertEquals('http://example.com/' in urls, True)
            self.assertEquals('http://m.example.com/' in urls, True)

