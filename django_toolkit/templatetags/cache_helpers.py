from django import template
from django.core.cache.utils import make_template_fragment_key
from django.core.cache import cache

register = template.Library()

@register.simple_tag
def expire_cache(fragment_name, *args):
    """
    Expire a cache item.
    
    @param url: The url object
    @param product_names: A list of product names
    @param start: The date from which the reporting should start.
    @param stop: The date at which the reporting should stop.
    """
    cache_key = make_template_fragment_key(fragment_name, args)
    cache.delete(cache_key)
    