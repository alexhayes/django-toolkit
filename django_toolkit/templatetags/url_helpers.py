from __future__ import absolute_import
from django import template
from ..url import shorten_url as _shorten_url
from ..url import netloc_no_www as _netloc_no_www

register = template.Library()


@register.simple_tag
def shorten_url(url, *args, **kwargs):
    if url:
        return _shorten_url(url, *args, **kwargs)


@register.filter
def netloc_no_www(url):
    if url:
        return _netloc_no_www(url)


@register.filter
def strip_protocol(url):
    if url:
        return url.replace('http://', '').replace('https://', '')

