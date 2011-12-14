from django.contrib.sites.models import get_current_site
from django.http import HttpResponse

class HttpResponseNotAuthorized(HttpResponse):
    status_code = 401

    def __init__(self, request, content=''):
        super(HttpResponseNotAuthorized, self).__init__(content)
        self['WWW-Authenticate'] = 'Basic realm="{}"'.format(get_current_site(request).name)
