from __future__ import absolute_import
from django import template
from ..url import shorten_url as _shorten_url
from ..url import netloc_no_www as _netloc_no_www

register = template.Library()


@register.filter
def shorten_url(url, length=32, strip_www=True):
    if url:
        return _shorten_url(url, length, strip_www)


@register.filter
def netloc_no_www(url):
    if url:
        return _netloc_no_www(url)

