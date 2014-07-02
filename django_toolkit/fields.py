from django.forms.models import ModelChoiceField
from django.forms.widgets import HiddenInput, MultipleHiddenInput
from django.forms.fields import EmailField
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.db.models.fields import CommaSeparatedIntegerField, TextField
import re
from django.core.validators import RegexValidator
from django.db.models.fields.subclassing import SubfieldBase
from django.db import models

class NoChoiceError(Exception): pass
class NoChoiceMatchError(Exception): pass

def ChoiceHumanReadable(choices, choice):
    """
    Return the human readable representation for a list of choices.
    
    @see https://docs.djangoproject.com/en/dev/ref/models/fields/#choices
    """
    if choice == None: raise NoChoiceError()
    for _choice in choices:
        if _choice[0] == choice:
            return _choice[1]
    raise NoChoiceMatchError("The choice '%s' does not exist in '%s'" % (choice, ", ".join([choice[0] for choice in choices])))

def ChoiceIndex(choices, choice):
    if choice == None: raise NoChoiceError()
    for i, _choice in enumerate(choices):
        if _choice[0] == choice:
            return i
    raise NoChoiceMatchError("The choice '%s' does not exist in '%s'" % (choice, ", ".join([choice[0] for choice in choices])))

class UserHumanNameModelChoiceField(ModelChoiceField):
    
    def label_from_instance(self, obj):
        return '%s %s' % (obj.first_name, obj.last_name)

class VisibleHiddenInput(HiddenInput):
    is_hidden = False

class VisibleMultipleHiddenInput(MultipleHiddenInput):
    is_hidden = False

class SeparatedValuesField(models.TextField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        self.separator = kwargs.pop('separator', ',')
        super(SeparatedValuesField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value: return
        if isinstance(value, list):
            return value
        return value.split(self.separator)

    def get_db_prep_value(self, value, connection=None, prepared=False):
        """Returns field's value prepared for interacting with the database
        backend.

        Used by the default implementations of ``get_db_prep_save``and
        `get_db_prep_lookup```
        """
        if not value:
            return
        if prepared:
            return value
        else:
            assert(isinstance(value, list) or isinstance(value, tuple))
            return self.separator.join([unicode(s) for s in value])

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

#class CommaSeparatedEmailField(TextField):
#    #__metaclass__ = SubfieldBase
#
#    def to_python(self, value):
#        print 'to_python', value
#        if not value:
#            return
#        if isinstance(value, list):
#            return value
#        return [address.strip() for address in value.split(',')]
#
#    def get_db_prep_value(self, value):
#        print 'get_db_prep_value', value
#        if not value:
#            return
#        return ','.join(unicode(s) for s in value)
#
#    def value_to_string(self, obj):
#        print 'value_to_string', obj
#        value = self._get_val_from_obj(obj)
#        return self.get_db_prep_value(value)
#
##    def formfield(self, **kwargs):
##        defaults = {'widget': MultiEmailField}
##        defaults.update(kwargs)
##        return super(CommaSeparatedEmailField, self).formfield(**defaults)

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["django_toolkit.fields.SeparatedValuesField"])

#class CommaSeparatedEmailField(EmailField):
#    default_validators = [validators.validate_email]
#    description = _("Comma-separated emails")
#
#    def formfield(self, **kwargs):
#        CommaSeparatedIntegerField
#        defaults = {
#            'error_messages': {
#                'invalid': _('Enter only email addresses separated by commas.'),
#            }
#        }
#        defaults.update(kwargs)
#        return super(CommaSeparatedEmailField, self).formfield(**defaults)