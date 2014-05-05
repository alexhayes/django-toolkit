from functools import wraps

def refresh(func):
    """
    Decorator that can be applied to model method that forces a refresh of the model.
    
    Note this decorator ensures the state of the model is what is currently within
    the database and therefore overwrites any current field changes.
    
    For example, assume we have the following model:
    
    .. code-block:: python
    
        class MyModel(models.Model):
            counter = models.IntegerField()
            
            @refresh
            def my_method(self):
                print counter
    
    Then the following is performed:
    
    .. code-block:: python
    
        i = MyModel.objects.create(counter=1)
        i.counter = 3
        i.my_method()
        # prints 1
        
    This behavior is useful in a distributed system, such as celery, where 
    "asserting the world is the responsibility of the task" - see http://celery.readthedocs.org/en/latest/userguide/tasks.html?highlight=model#state
    
    Note that the refresh of the model uses the approach outlined in https://github.com/planop/django/blob/ticket_901/django/db/models/base.py#L1012
    which was discovered after from https://code.djangoproject.com/ticket/901#comment:29
    which is a Django ticket which discusses a specific method 'refresh' on a 
    model.
    """
    
    @wraps(func)
    def inner(self, *args, **kwargs):
        # Refresh the model instance - see https://github.com/planop/django/blob/ticket_901/django/db/models/base.py#L1012
        new_self = self.__class__._base_manager.using(self._state.db).get(pk=self.pk)
        for f in self.__class__._meta.fields:
            setattr(self, f.name, getattr(new_self, f.name))
        return func(self, *args, **kwargs)
    return inner