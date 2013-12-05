
def get_object_comment_reference(instance, title=None):
    """
    Get an object reference for use within a comment so that it can be programatically
    referenced in the future (by a machine parsing the HTML...).
    """
    span = '<span data-object-type="%s.%s" data-object-pk="%s">%s</span>' % (
        instance.__module__,
        instance.__class__.__name__,
        instance.pk,
        instance if title is None else title
    )
    try:
        return '<a href="%s">%s</a>' % (
            instance.get_absolute_url(),
            span
        )
    except AttributeError:
        return span