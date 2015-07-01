from __future__ import absolute_import
from __future__ import print_function
import requests

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse


DESKTOP_USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:10.0.2) Gecko/20100101 Firefox/10.0.2'
MOBILE_USER_AGENT = 'Mozilla/5.0 (Linux; Android 4.2.2; GT-I9505 Build/JDQ39) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.59 Mobile Safari/537.36'


def url_with_protocol(url):
    if '://' not in url:
        return 'http://%s' % url
    else:
        return url


def resolve_url(url, desktop_user_agent=None, mobile_user_agent=None):
    """
    Url Resolver
    Given a url a list of resolved urls is returned for desktop and mobile user agents
    """
    if not desktop_user_agent:
        desktop_user_agent = DESKTOP_USER_AGENT
    if not mobile_user_agent:
        mobile_user_agent = MOBILE_USER_AGENT

    input_urls = set()

    parsed = urlparse(url_with_protocol(url))
    netloc = parsed.netloc

    if netloc.startswith('www.'):
        netloc = netloc[4:]

    input_urls.add('http://%s%s' % (netloc, parsed.path if parsed.path else '/'))
    input_urls.add('http://www.%s%s' % (netloc, parsed.path if parsed.path else '/'))

    resolved_urls = set()

    for input_url in input_urls:
        desktop_request = requests.get(input_url, headers={'User-Agent': desktop_user_agent})
        resolved_urls.add(desktop_request.url)
        mobile_request = requests.get(input_url, headers={'User-Agent': mobile_user_agent})
        resolved_urls.add(mobile_request.url)

    return list(resolved_urls)
