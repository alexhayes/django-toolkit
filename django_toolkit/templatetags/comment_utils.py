from django import template
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib import comments
from django.utils import six
from django.utils.deprecation import RenameMethodsBase
from django.utils.encoding import smart_text
from django.contrib.comments.templatetags.comments import RenderCommentListNode

register = template.Library()

class ReversedRenderCommentListNode(RenderCommentListNode):
    def get_queryset(self, context):
        qs = RenderCommentListNode.get_queryset(self, context)
        return qs.order_by('-submit_date')

@register.tag
def render_reversed_comment_list(parser, token):
    """
    Render the comment list (as returned by ``{% get_comment_list %}``)
    through the ``comments/list.html`` template

    Syntax::

        {% render_comment_list for [object] %}
        {% render_comment_list for [app].[model] [object_id] %}

    Example usage::

        {% render_comment_list for event %}

    """
    return ReversedRenderCommentListNode.handle_token(parser, token)