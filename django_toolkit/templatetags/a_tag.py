from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def a(value):
    if value:
        return mark_safe('<a href="%s">%s</a>' % (value, value))

@register.filter
def a_blank(value):
    if value:
        return mark_safe('<a href="%s" target="_blank">%s</a>' % (value, value))

@register.filter
def a_tel(value):
    if value:
        return mark_safe('<a href="tel:%s">%s</a>' % (value, value))

@register.filter
def a_email(value):
    if value:
        return mark_safe('<a href="mailto:%s">%s</a>' % (value, value))