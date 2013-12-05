from crispy_forms.bootstrap import AppendedText
from django.forms.widgets import SelectMultiple, TextInput
from datetime import datetime

class DateTimePickerField(AppendedText):
    
    def __init__(self, field, text='<i data-time-icon="icon-time" data-date-icon="icon-calendar"></i>', 
                 css_class='datetimeinput datetimeinput-picker', extra_css_class='',
                 *args, **kwargs):
        css_class += ' ' + extra_css_class
        super(DateTimePickerField, self).__init__(field, text=text, 
                                                  css_class=css_class, 
                                                  *args, **kwargs)

class DatePickerField(AppendedText):
    
    def __init__(self, field, text='<i data-time-icon="icon-time" data-date-icon="icon-calendar"></i>', 
                 css_class='dateinput dateinput-picker', extra_css_class='', 
                 *args, **kwargs):
        css_class += ' ' + extra_css_class
        super(DatePickerField, self).__init__(field, text=text, 
                                              css_class=css_class, 
                                              *args, **kwargs)

class DurationPickerField(AppendedText):
    
    def __init__(self, field, text='<i data-time-icon="icon-time" data-date-icon="icon-calendar"></i>', 
                 css_class='durationinput durationinput-picker', extra_css_class='',
                 *args, **kwargs):
        css_class += ' ' + extra_css_class
        super(DurationPickerField, self).__init__(field, text=text, 
                                                  css_class=css_class,
                                                  *args, **kwargs)

class MonthPickerField(AppendedText):
    
    def __init__(self, field, text='<i class="icon-calendar"></i>', 
                 css_class='monthinput monthinput-picker', extra_css_class='',
                 *args, **kwargs):
        css_class += ' ' + extra_css_class
        super(MonthPickerField, self).__init__(field, text=text, 
                                                  css_class=css_class,
                                                  *args, **kwargs)

class CommaSeparatedInput(TextInput):
    
    def render(self, name, value, attrs=None):
        str_value = ",".join(value) if isinstance(value, list) else value
        return super(CommaSeparatedInput, self).render(name=name, value=str_value, attrs=attrs)
