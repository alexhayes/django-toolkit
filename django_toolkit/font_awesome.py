from django.core.urlresolvers import reverse

class Icon():
    """
    Represents a Bootstrap icon (<i>) tag.
    """
    
    def __init__(self, icon, *css):
        self.icon = icon
        self.css = css

    def render(self, extra_css=[]):
        html = '<i class="%s' % self.icon
        if self.css:
            html += ' %s' % ' '.join([css for css in self.css])
        if extra_css:
            html += ' %s' % ' '.join([css for css in extra_css])
        html += '"></i>'
        return html

class BaseCollection():
    
    def __init__(self, *items):
        self.items = list(items)
    
    def append(self, item):
        self.items.append(item)

class Stack(BaseCollection):
    """
    Represents a Font Awesome icon stack.
    
    @see http://fortawesome.github.io/Font-Awesome/examples/ 
    """
    
    def render(self):
        """
        Render the icon stack.
        
        For example:
        <span class="icon-stack">
          <i class="icon-check-empty icon-stack-base"></i>
          <i class="icon-twitter"></i>
        </span>
        <span class="icon-stack">
          <i class="icon-circle icon-stack-base"></i>
          <i class="icon-flag icon-light"></i>
        </span>
        <span class="icon-stack">
          <i class="icon-sign-blank icon-stack-base"></i>
          <i class="icon-terminal icon-light"></i>
        </span>
        <span class="icon-stack">
          <i class="icon-camera"></i>
          <i class="icon-ban-circle icon-stack-base text-error"></i>
        </span>
        """
        return '<span class="icon-stack">%s</span>' % (
            ''.join([item.render(['icon-stack-base'] if i == 0 else []) for (i, item) in enumerate(self.items)])
        )

class ButtonGroup(BaseCollection):
    """
    Font-Awesome ButtonGroup
    
    @see http://fortawesome.github.io/Font-Awesome/examples/
    """
    
    def render(self):
        """
        Render the groups.
        
        Example:
        <div class="btn-group">
          <a class="btn" href="#"><i class="icon-align-left"></i></a>
          <a class="btn" href="#"><i class="icon-align-center"></i></a>
          <a class="btn" href="#"><i class="icon-align-right"></i></a>
          <a class="btn" href="#"><i class="icon-align-justify"></i></a>
        </div>
        """
        return '<div class="btn-group">%s</div>' % (
            ''.join([item.render() for (i, item) in enumerate(self.items)])
        )

class Button():
    
    def __init__(self, inner=None, data_tip=None,
                 view=None, view_kwargs=[], view_args=[], next=None,
                 href=None, 
                 title=None, a_attrs={}, target=False,
                 modal=False, data_target=False):
        self.inner = inner
        self.href = href
        self.view = view
        self.view_args = view_args
        self.view_kwargs = view_kwargs
        self.title = title
        self.a_attrs = a_attrs
        self.next = next
        self.modal = modal
        self.data_tip = data_tip
        self.target = target
    
    def render(self):
        """
        <a class="btn" href="#"><i class="icon-repeat"></i> Reload</a>
        """
        html = ''
        href = self.view if self.view is not None else self.href
        if href:
            a_attrs = self.a_attrs
            if self.view:
                href = reverse(self.view, args=self.view_args, kwargs=self.view_kwargs)
            if self.next:
                href += '?next=%s' % (self.next if self.next.startswith('/') else reverse(self.next))
            if self.modal:
                a_attrs['role'] = "button"
                a_attrs['data-toggle'] = "modal"
                a_attrs['data-remoteinbody'] = "false"
                if self.data_target:
                    if isinstance(self.data_target, basestring):
                        a_attrs['data-target'] = self.data_target
                    else:
                        a_attrs['data-target'] = "#modal"
            if self.data_tip:
                a_attrs['data-tip'] = self.data_tip
            if self.target:
                a_attrs['target'] = self.target
            if 'css_class' not in a_attrs:
                a_attrs['css_class'] = ''
            a_attrs['css_class'] += ' btn'
            a_attrs = ' '.join(['%s="%s"' % (key if key != 'css_class' else 'class', value) for key,value in a_attrs.iteritems()])
            html += '<a href="%s" %s>' % (href, a_attrs)
        
        if hasattr(self.inner, 'render'):
            html += self.inner.render()
        else:
            html += self.inner
        
        if self.title:
            html += self.title
        
        if href:
            html += "</a>"
        
        return html
            
        
    