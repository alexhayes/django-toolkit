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
    """

    @wraps(func)
    def inner(self, *args, **kwargs):
        self = self.__class__.objects.get(pk=self.pk)
        return func(self, *args, **kwargs)
    return inner