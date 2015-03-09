from functools import wraps

def ensure_self(func):
    """
    Decorator that can be used to ensure 'self' is the first argument on a task method.

    This only needs to be used with task methods that are used as a callback to
    a chord or in link_error and is really just a hack to get around https://github.com/celery/celery/issues/2137

    Usage:

    .. code-block:: python

        class Foo(models.Model):

            def __init__(self):
                self.bar = 1

            @task
            def first(self):
                pass

            @task
            @ensure_self
            def last(self, results=None):
                print self.bar

    Then the following is performed:

    .. code-block:: python

        f = Foo()
        (f.first.s() | f.last.s(this=f)).apply_async()
        # prints 1

    The important part here is that 'this' is passed into the last.s subtask.

    Hopefully issue 2137 is recognized as an issue and fixed and this hack is
    no longer required.
    """

    @wraps(func)
    def inner(*args, **kwargs):
        try:
            self = kwargs.pop('this')
            if len(args) >= 1 and self == args[0]:
                # Make the assumption that the first argument hasn't been passed in twice...
                raise KeyError()
            return func(self, *args, **kwargs)
        except KeyError:
            # 'this' wasn't passed, all we can do is assume normal innovation
            return func(*args, **kwargs)
    return inner
