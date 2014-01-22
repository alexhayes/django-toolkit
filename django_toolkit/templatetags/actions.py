from django import template
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def actions(obj, **kwargs):
    """
    Return actions available for an object
    """
    if 'exclude' in kwargs:
        kwargs['exclude'] = kwargs['exclude'].split(',')
    actions = obj.get_actions(**kwargs)
    if isinstance(actions, dict):
        actions = actions.values()
    buttons = "".join("%s" % action.render() for action in actions)
    return '<div class="actions">%s</div>' % buttons
