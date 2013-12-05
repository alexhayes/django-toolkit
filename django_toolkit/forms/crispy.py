from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, TEMPLATE_PACK, Field
from django.forms.fields import DateField, DateTimeField, CharField
from durationfield.forms.fields import DurationField
from django_toolkit.forms.widgets import DatePickerField, DateTimePickerField,\
    DurationPickerField
from django.forms.forms import BoundField
from django.utils.safestring import mark_safe

class SpecialFieldsFormHelper(FormHelper):
    """
    A form helper that automatically uses DatePickerField, DateTimePickerField and DurationPickerField fields.
    """
    
    def build_default_layout(self, form):
        fields = []
        for name, field in form.fields.iteritems():
            fields.append(get_crispy_field_helper(name, field))
        return Layout(*fields)
    
    def render_layout(self, form, context, template_pack=TEMPLATE_PACK):
        self.layout = self.build_default_layout(form) 
        return super(SpecialFieldsFormHelper, self).render_layout(form, context, template_pack)

def get_crispy_field_helper(name, field):
    if isinstance(field, DateField):
        return DatePickerField(name)
    elif isinstance(field, DateTimeField):
        return DateTimePickerField(name)
    elif isinstance(field, DurationField):
        return DurationPickerField(name)
    else:
        return Field(name)
    
class VisibleHiddenField(Field):
    
    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK):
        extra = []
        for field in self.fields:
            field_instance = form.fields[field]
            bound_field = BoundField(form, field_instance, field)
            extra.append(bound_field.value())
        context['extra'] = mark_safe("\n".join(extra))
        return super(VisibleHiddenField, self).render(form, form_style, context, template_pack)
