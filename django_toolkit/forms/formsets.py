from django.forms.formsets import DELETION_FIELD_NAME
from django.forms.widgets import HiddenInput
from django.forms.models import BaseModelFormSet

class HiddenDeleteModelFormSet(BaseModelFormSet):
    
    def add_fields(self, form, index):
        super(HiddenDeleteModelFormSet, self).add_fields(form, index)
        
        form.fields[DELETION_FIELD_NAME].widget = HiddenInput()