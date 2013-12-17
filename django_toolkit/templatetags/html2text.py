from __future__ import absolute_import
import html2text as _html2text
from django import template

register = template.Library()

@register.filter
def html2text(value):
    """
    Uses html2text to convert HTML to text...
    """
    return _html2text.html2text(value)