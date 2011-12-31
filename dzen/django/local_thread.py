try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

_thread_locals = local()

def current_request():
    return getattr(_thread_locals, 'request', None)

class LocalThreadRequestMiddleware(object):
    def process_request(self, request):
        _thread_locals.request = request
