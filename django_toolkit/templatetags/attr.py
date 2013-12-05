import re
from django import template
from django.conf import settings

numeric_test = re.compile("^\d+$")
register = template.Library()

@register.filter(name='getattribute')
def getattribute(value, arg):
    """Gets an attribute of an object dynamically from a string name"""
    
    if callable(getattr(value, arg)):
        return str(getattr(value, arg)())
    elif hasattr(value, str(arg)):
        return getattr(value, arg)
    elif hasattr(value, 'has_key') and value.has_key(arg):
        return value[arg]
    elif numeric_test.match(str(arg)) and len(value) > int(arg):
        return value[int(arg)]
    elif arg in dir(value):
        return getattr(value, arg)()
    else:
        return settings.TEMPLATE_STRING_IF_INVALID