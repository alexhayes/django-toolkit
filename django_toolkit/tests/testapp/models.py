from django.db import models
from django.db.models.query import QuerySet
from django_toolkit.db.models import QuerySetManager


class ModelWithChainedQuerySet(models.Model):
    foo = models.BooleanField(default=False)
    bar = models.BooleanField(default=False)

    objects = QuerySetManager()

    def __unicode__(self):
        return u'%s' % self.pk

    class QuerySet(QuerySet):

        def is_foo(self):
            return self.filter(foo=True)

        def is_bar(self):
            return self.filter(bar=True)

        def is_not_foo(self):
            return self.filter(foo=False)

        def is_not_bar(self):
            return self.filter(bar=False)
