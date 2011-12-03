from django.contrib.sites.models import get_current_site
from django.http import HttpResponse

class HttpResponseNotAuthorized(HttpResponse):
    status_code = 401

    def __init__(self, request):
        super(HttpResponseNotAuthorized, self).__init__()
        self['WWW-Authenticate'] = 'Basic realm="{}"'.format(get_current_site(request).name)
