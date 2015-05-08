from __future__ import absolute_import
import json
import os
import magic
from django.views.generic import DeleteView
from django.views.generic.base import View, RedirectView, ContextMixin
from django.core.servers.basehttp import FileWrapper
from django.http.response import HttpResponse
from django.utils.encoding import smart_str
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView, ModelFormMixin,\
    FormMixin
from django.core.urlresolvers import reverse
from django.contrib import messages
from django_toolkit.decorators import class_login_required
from django.conf import settings
from django.utils.importlib import import_module
from django.core.serializers.json import DjangoJSONEncoder
from django.views.generic.dates import YearMixin, MonthMixin, DayMixin,\
    _date_from_string
import collections
from django.core.exceptions import ValidationError

JSON_ENCODER = getattr(settings, 'JSON_ENCODER', False)
if JSON_ENCODER:
    parts = JSON_ENCODER.split('.')
    module = import_module('.'.join(parts[:-1]))
    JSON_ENCODER = getattr(module, parts[-1:][0])
else:
    JSON_ENCODER = DjangoJSONEncoder

def error_handler_404(request):
    """
    500 error handler which includes ``request`` in the context.

    Templates: `500.html`
    Context: None
    """
    from django.template import Context, loader
    from django.http import HttpResponseServerError

    t = loader.get_template('404.html')
    return HttpResponseServerError(t.render(Context({
        'request': request,
        'settings': settings,
    })))

def error_handler_500(request):
    """
    500 error handler which includes ``request`` in the context.

    Templates: `500.html`
    Context: None
    """
    from django.template import Context, loader
    from django.http import HttpResponseServerError

    t = loader.get_template('500.html')
    return HttpResponseServerError(t.render(Context({
        'request': request,
        'settings': settings,
    })))

class RedirectNextDeleteView(DeleteView):
    """
    Generic view that redirects to request next parameter - if set.
    """
    success_view = False
    permanent_delete = True
    template_name = 'generic/confirm_delete.html'
    
    def get_context_data(self, **kwargs):
        kwargs.update(permanent_delete=self.permanent_delete)
        return super(RedirectNextDeleteView, self).get_context_data(**kwargs)
    
    def get_success_url(self):
        if self.request.POST.has_key('next'):
            return self.request.POST.get('next')
        if self.success_view:
            return reverse(self.success_view)
        return DeleteView.get_success_url(self) 

    def render_to_response(self, context, **response_kwargs):
        if self.request.REQUEST.get('next', False):
            context['next'] = self.request.REQUEST.get('next')
        elif self.success_view:
            context['next'] = reverse(self.success_view)
        elif self.request.META.get('HTTP_REFERER', False):
            # Note that if this is the object being deleted it won't work, but what other option do we have...
            context['next'] = self.request.META.get('HTTP_REFERER')
        return DeleteView.render_to_response(self, context, **response_kwargs)

class RedirectNextOrBackView(RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        """
        Redirect to request parameter 'next' or to referrer if url is not defined. 
        """
        if self.request.REQUEST.has_key('next'): 
            return self.request.REQUEST.get('next')
        url = RedirectView.get_redirect_url(self, **kwargs)
        if url:
            return url
        return self.request.META.get('HTTP_REFERER')

class FileDownloadView(View):
    """
    Generic view that supports downloading of files.
    """
    xsend = False
    attachment = True
    file = None
    force_download = True
    no_cache = True
    
    def filepath(self):
        if self.file:
            return self.file
        raise NotImplementedError()

    def openfile(self):
        return open(self.filepath())
    
    def filesize(self):
        return os.path.getsize(self.filepath())
    
    def filename(self):
        return os.path.basename(self.filepath())
    
    def content_type(self):
        return magic.from_file(self.filepath(), mime=True)
    
    def headers(self, response):
        response['Accept-Ranges'] = 'bytes'
        response['Content-Length'] = self.filesize()
        if self.force_download:
            response['Content-Disposition'] = '%sfilename="%s"' % ('attachment;' if self.attachment else '', self.filename())
        if self.no_cache:
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = 0
        if self.xsend:
            response['X-Sendfile'] = smart_str(self.filepath())
        return response
    
    def render_to_response(self, context=False):
        """Send file to client."""
        f = self.openfile()
        wrapper = FileWrapper(f)
        response = HttpResponse(wrapper, content_type=self.content_type())
        self.headers(response)
        return response

class DetailFileDownloadView(FileDownloadView, DetailView):
    file_field = False

    def filepath(self):
        return getattr(self.object, self.file_field).path

class GetFileDownloadView(FileDownloadView):
    
    def get(self, request, *args, **kwargs):
        return self.render_to_response()

class FormAcceptsRequestMixin(FormMixin):
    form_accepts_request = False
    
    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super(FormAcceptsRequestMixin, self).get_form_kwargs()
        if self.form_accepts_request:
            kwargs.update({'request': self.request})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(FormAcceptsRequestMixin, self).get_context_data(**kwargs)
        return context

class GenericCreateView(FormAcceptsRequestMixin, CreateView):
    template_name='generic/create.html'

    def get_success_url(self):
        if self.request.REQUEST.has_key('next'): 
            return self.request.REQUEST.get('next')
        else:
            return super(GenericCreateView, self).get_success_url()

class GenericUpdateView(FormAcceptsRequestMixin, UpdateView):
    template_name='generic/update.html'

    def get_success_url(self):
        if self.request.REQUEST.has_key('next'): 
            return self.request.REQUEST.get('next')
        else:
            return super(GenericUpdateView, self).get_success_url()

class GenericDeleteView(DeleteView):
    template_name='generic/delete.html'

    def get_context_data(self, **kwargs):
        context = DeleteView.get_context_data(self, **kwargs)
        if self.breadcrumbs:
            context['breadcrumbs'] = []
            for breadcrumb in self.breadcrumbs:
                if 'title' not in breadcrumb:
                    breadcrumb['title'] = self.object
                context['breadcrumbs'].append({
                    'href': reverse(breadcrumb['viewname']),
                    'title': breadcrumb['title']
                })
            context['breadcrumbs'].append({
                'href': self.object.get_absolute_url(),
                'title': self.object
            })
            context['breadcrumbs'].append({
                'href': self.request.path,
                'title': 'Update'
            })
        return context

@class_login_required
class LoginRequiredDetailView(DetailView): pass

@class_login_required
class LoginRequiredCreateView(GenericCreateView): pass

@class_login_required
class LoginRequiredUpdateView(GenericUpdateView): pass

@class_login_required
class LoginRequiredDeleteView(GenericDeleteView): pass

class AjaxMixin(object):
    """
    Provides helper methods around determining if we're using ajax.
    """
    def is_ajax(self):
        return self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    
    def accepts_json(self):
        return 'json' in self.request.META.get('HTTP_ACCEPT', []) or self.request.REQUEST.get('json', False) != False
    
    def render_to_response(self, context, **response_kwargs):
        """
        Returns a response, using the `response_class` for this
        view, with a template rendered with the given context.

        If any keyword arguments are provided, they will be
        passed to the constructor of the response class.
        """
        return HttpResponse(json.dumps(context, cls=JSON_ENCODER), 
                            content_type='application/json',
                            **response_kwargs)

class ModelCallMethodsView(SingleObjectMixin, RedirectNextOrBackView):
    """
    Call methods on a model and then redirect.
    """
    permanent = False
    # A list of methods that should be called
    methods = []
    # A list of errors that should be ignored
    expect = []
    # A success_message to add to the messages stack
    success_messages = None
    # Outcomes/return from each method call
    outcomes = {}
    
    def callable_args(self, request, *args, **kwargs):
        return {}
    
    def callable_kwargs(self, request, *args, **kwargs):
        return {}

    def get_callable(self, obj, method):
        return getattr(obj, method)

    def call(self, obj, method, request, *args, **kwargs):
        return self.get_callable(obj, method)(*self.callable_args(request, *args, **kwargs),
                                              **self.callable_kwargs(request, *args, **kwargs))

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            if isinstance(self.methods, dict):
                for (method, method_kwargs) in self.methods.items():
                    getattr(self.object, method)(**method_kwargs)
            else:
                for method in self.methods:
                    self.outcomes[method] = self.call(self.object, method, request, *args, **kwargs)

            # Redirect back or next
            if self.success_messages:
                if isinstance(self.success_messages, collections.Iterable):
                    for message, level in self.success_messages:
                        messages.add_message(request, level, message)
                else:
                    messages.success(request, self.success_message)

            return RedirectNextOrBackView.get(self, request, *args, **kwargs)
        except Exception as e:
            if isinstance(e, ValidationError):
                for message in e.messages:
                    messages.add_message(request, messages.ERROR, message)
                return RedirectNextOrBackView.get(self, request, *args, **kwargs)
            elif len([expect for expect in self.expect if isinstance(e, expect)]) > 0:
                messages.add_message(request, messages.ERROR, e)
                return RedirectNextOrBackView.get(self, request, *args, **kwargs)
            else:
                # If we don't expect this exception, raise it.
                raise


class CeleryAsyncModelCallMethodsView(ModelCallMethodsView):
    
    def call(self, obj, method, request, *args, **kwargs):
        call_args = self.callable_args(request, *args, **kwargs)
        call_kwargs = self.callable_kwargs(request, *args, **kwargs)
        return self.get_callable(obj, method).s(*call_args, **call_kwargs).apply_async()

class AcceptsUserModelCallMethodsView(ModelCallMethodsView):
    
    def callable_kwargs(self, request, *args, **kwargs):
        kwargs = ModelCallMethodsView.callable_kwargs(self, request, *args, **kwargs)
        kwargs.update(user=request.user)
        return kwargs

@class_login_required
class LoginRequiredModelCallMethodsView(ModelCallMethodsView): pass

class NamedUrlRedirectView(RedirectView):

    def get_redirect_url(self, **kwargs):
        return reverse(self.url)

class BaseDayView(YearMixin, MonthMixin, DayMixin):
    """
    List of objects published on a given day.
    """
    def get_date(self):
        """
        Return (date_list, items, extra_context) for this request.
        """
        year = self.get_year()
        month = self.get_month()
        day = self.get_day()

        return _date_from_string(year, self.get_year_format(),
                                 month, self.get_month_format(),
                                 day, self.get_day_format())

class ModelExtraContextMixin(View):
    """
    A DetailView that gets extra context from the model. 
    """
    
    def get_context_data(self, **kwargs):
        context = super(ModelExtraContextMixin, self).get_context_data(**kwargs)
        if self.object and hasattr(self.object, 'detail_view_context'):
            context.update(**self.object.detail_view_context(self))
        return context

class ModelExtraContextDetailView(ModelExtraContextMixin, DetailView): pass
class ModelExtraContextUpdateView(ModelExtraContextMixin, GenericUpdateView): pass

class XEditableGenericUpdateView(GenericUpdateView, AjaxMixin):
    """
    A view that can be used with jQuery plugin X-Editable to process updates on a single field.
    
    For example:

        # models.py

        {{{#!python
        class Car(models.Model):
            ...
            color = models.CharField(max_length=128)
            ...
        }}}
    
        # forms.py
        
        {{{#!python
        class SetColourForm(forms.ModelForm):
            class Meta:
                model = Car
                fields = ('colour',)
        }}}
      
        # urls.py
        
        {{{#!python
        url(r'^car/(?P<pk>\d+)/set-colour/$', 
            view=permission_required_raise('cars.change_car')(XEditableGenericUpdateView.as_view(
                model=Car,
                form_class=SetColourForm,
                field_name='colour',    
            )),
            name="cars:car:setcolour", 
        )
        }}}
    
        # init.js
        
        {{{#!js
        $('#color').editable({
            params: function(params) {  //params already contain `name`, `value` and `pk`
                var data = {};
                data[params.name] = params.value;
                return data;
            },
            success: function(response, newValue) {
                if(!response.success) return response.msg; //msg will be shown in editable form
            }
        });
        }}}
        
    :see: http://vitalets.github.io/x-editable/docs.html
    """
    
    field_name = None
    
    def form_invalid(self, form):
        if self.is_ajax():
            errors = form.errors  #: :type errors: ErrorDict
            context = dict(success=False, 
                           msg=",".join([v.as_text() for k, v in errors.items()]))
            return AjaxMixin.render_to_response(self, context)
        else:
            return GenericUpdateView.form_invalid(self, form)
    
    def form_valid(self, form):
        if self.is_ajax():
            self.object = form.save()
            context = dict(success=True, newValue=self.new_value(self.object))
            return AjaxMixin.render_to_response(self, context)
        else:
            return GenericUpdateView.form_valid(self, form)

    def new_value(self, obj):
        return getattr(obj, self.field_name)