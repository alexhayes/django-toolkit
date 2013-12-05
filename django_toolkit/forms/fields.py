from crispy_forms.layout import Field, TEMPLATE_PACK
from django_toolkit.templatetags.foreign_a import foreign_a
from django.utils.safestring import mark_safe
from django.forms.forms import BoundField
from django import forms
from django.core.validators import validate_email
from django_toolkit.forms.widgets import CommaSeparatedInput

class ToField(Field):
    
    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK):
        extra = []
        for field in self.fields:
            extra.append('<ul>')
            field_instance = form.fields[field]
            bound_field = BoundField(form, field_instance, field)
            for contact in bound_field.field.queryset:
                extra.append('<li>%s &lt;<a href="mailto:%s">%s</a>&gt;</li>' % (foreign_a(contact), contact.email, contact.email))
            extra.append('</ul>')
        context['extra'] = mark_safe("\n".join(extra))
        return super(ToField, self).render(form, form_style, context, template_pack)

class MultiEmailField(forms.Field):
    widget = CommaSeparatedInput

    def __init__(self, help_text='Separate email addresses with a comma.', *args, **kwargs):
        super(MultiEmailField, self).__init__(help_text=help_text, *args, **kwargs)

    def to_python(self, value):
        "Normalize data to a list of strings."

        # Return an empty list if no input was given.
        if not value:
            return []
        return value.split(',')

    def validate(self, value):
        "Check if value consists only of valid emails."

        # Use the parent's handling of required fields, etc.
        super(MultiEmailField, self).validate(value)

        for email in value:
            validate_email(email)