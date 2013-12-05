import time
import warnings
from datetime import date, datetime
from django.db import models
from django.core import validators
from django.conf import settings
from django.utils import timezone

# see https://code.djangoproject.com/ticket/12276

class UnixDateTimeField(models.DateTimeField):
    """
    UnixTimeStamp field conversion to datetime. 
    """

    __metaclass__ = models.SubfieldBase

    def __init__(self, zero_null=False, is_utc=True, *args, **kwargs):
        """
        @param zero_null: Set to true if 0 values in the database should be translated 
                          to None in python.
        @param is_utc:    Set to True if date is stored as UTC. Of course, unixtimestamp 
                          implies that it would be, however some systems store 
                          as localtime.
        """
        super(UnixDateTimeField, self).__init__(*args, **kwargs)
        self.zero_null = zero_null
        self.is_utc = is_utc

    def get_internal_type(self):
        return 'PositiveIntegerField'

    def to_python(self, value):
        if value is None or isinstance(value, datetime):
            return value
        if isinstance(value, date):
            return datetime(value.year, value.month, value.day)
        if isinstance(value, basestring) and len(value) == 0:
            return None
        if value == 0 and self.zero_null:
            return None
        value = datetime.fromtimestamp(float(value))
        if settings.USE_TZ:
            if self.is_utc:
                # It's a unixtimestamp, it *should* be utc
                value = timezone.make_aware(value, timezone.utc)
            else:
                # Even tho is a unixtimestamp, it's probably entered by something that isn't entering unixtime
                default_timezone = timezone.get_default_timezone()
                value = timezone.make_aware(value, default_timezone)
        return value
    
    def get_db_prep_value(self, value, connection, prepared=False):
        if value == None:
            if self.zero_null:
                return '0'
            return None
        return int(time.mktime(value.timetuple()))

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        python_value = self.to_python(value)
        if isinstance(python_value, datetime):
            return self.to_python(value).strftime('%Y-%m-%d %H:%M:%S')
        else:
            return '%s' % python_value

    def get_lookup_constraint(self, constraint_class, alias, targets, sources, lookup_type,
                              raw_value):
        from django.db.models.sql.where import Constraint
        assert len(targets) == len(sources)
        
        if lookup_type == 'isnull' and self.zero_null and raw_value:
            return (Constraint(alias, targets[0].column, targets[0]), 'exact', None)
        else:
            return (Constraint(alias, targets[0].column, self), lookup_type, raw_value)

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^django_toolkit\.db\.fields\.UnixDateTimeField"])
