from django.contrib.auth.decorators import login_required as django_login_required,\
    permission_required

"""
Patch view decorators.

@see http://stackoverflow.com/questions/6069070/how-to-use-permission-required-decorators-on-django-class-based-views
"""
from django.utils.decorators import method_decorator
from inspect import isfunction

class _cbv_decorate(object):
    def __init__(self, dec):
        self.dec = method_decorator(dec)

    def __call__(self, obj):
        obj.dispatch = self.dec(obj.dispatch)
        return obj

def patch_view_decorator(dec):
    def _conditional(view):
        if isfunction(view):
            return dec(view)

        return _cbv_decorate(dec)(view)

    return _conditional

class_login_required = patch_view_decorator(django_login_required)

def permission_required_raise(perm, login_url=None, raise_exception=True):
    """
    A permission_required decorator that raises by default.
    """
    return permission_required(perm, login_url=login_url, raise_exception=raise_exception)