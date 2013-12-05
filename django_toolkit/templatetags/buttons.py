from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def button_with_image(size='medium', icon=None, text=None, title=None, button=False, 
                      name=None, target=False, disabled=False, extra_css=None, modal=None, 
                      data_target='#modal', viewname=None, next=None, extra_href=False, href=False,
                      fancyajax=False, viewargs=[], **kwargs):
    """
    Output a button using Bingo's button html.
    
    @param size: The size that refers to the icon css class.
    @param icon: A css class that refers to an icon - for example 'send_mail'
    @param text: Text to display on the button
    @param title: Title parameter for the button or if button=False the data-tip for an a tag. 
    @param button: If true a button tag will be returned.
    @param name: A name for the button
    @param target: A target for the a tag
    @param disabled: If true, css class 'disabled' will be added to the container div.
    @param extra_css: A string of extra css classes.
    @param model: If True the class 'model' is placed on the a tag.
    @param viewname: The django viewname as defined in a urls.py file.
    @param **kwargs: Remaining keyword args are supplied to django.core.urlresolvers.reverse
    @param next: If specified ?next=[NEXT] will be appended to any generated link.
    @return string 
    """
    html = '<div class="button-std'
    
    if disabled:
        html += ' disabled'
    
    html += '">'
    
    if button:
        html += '<button type="submit" name="%s" value="%s" class="%s">' % (name, title, icon)
        if icon:
            html += '<span class="icon-%s icon-%s-%s"></span>' % (size, size, icon)
        html += '<span>%s</span></button>' % (title)
    else:
        html += '<a class="%s' % (icon)
        if fancyajax:
            html += ' fancybox fancybox.ajax'
        if extra_css:
            html += ' %s' % (extra_css)
        html += '"'
        if modal:
            html += ' role="button" data-toggle="modal" data-remoteinbody="false"'
            if data_target:
                html += ' data-target="#modal"'
        if fancyajax:
            html += ' data-spinner-append="1"'
        if viewname:
            html += ' href="%s' % (reverse(viewname, args=viewargs, kwargs=kwargs))
        elif href:
            html += ' href="%s' % (href)
        if viewname or href:
            if next:
                if next.startswith('/'):
                    html += '?next=%s' % next
                else:
                    html += '?next=%s' % reverse(next)
            if extra_href:
                html += extra_href
            html += '"'
        if not title and text:
            title = text
        if title:
            html += ' data-tip="%s"' % (title)
        if target:
            html += ' target="%s"' % (target)
        html += '>'
        
        if icon:
            html += '<span class="icon-%s icon-%s-%s"></span>' % (size, size, icon)
        
        if text:
            html += '<span class="title">%s</span>' % (text)
    
        html += '</a></div>'
    
    return html

@register.simple_tag
def button(type='submit', title='Submit', css="btn"):
    return '<button type="%s" class="%s"><span>%s</span></button>' % (type, css, title)

@register.simple_tag
def imageonlybutton(icon, title, viewname=None, **kwargs):
    return button_with_image(icon=icon, title=title, viewname=viewname, **kwargs)

