from django import http
from django.contrib.auth.decorators import login_required
from django.utils import simplejson as json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

def handler404(request):
    pass

def handler500(request):
    pass

class CSRFExemptMixin(object):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CSRFExemptMixin, self).dispatch(*args, **kwargs)

class ProtectedViewMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProtectedViewMixin, self).dispatch(*args, **kwargs)

class JSONResponseMixin(object):
    def render_to_response(self, context, **kwargs):
        "Returns a JSON response containing 'context' as payload"
        return self.get_json_response(self.convert_context_to_json(context), **kwargs)

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return http.HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        return json.dumps(context)
