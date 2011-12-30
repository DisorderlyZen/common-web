try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

_thread_locals = local()

@property
def current_request():
    return getattr(_thread_locals, 'request', None)

class LocalThreadRequestMiddleware(object):
    def process_request(request):
        _thread_locals.request = request
