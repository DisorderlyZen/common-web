from django.conf import settings

ANALYTICS_KEY = 'GOOGLE_ANALYTICS_ID'

def analytics(request):
    return {ANALYTICS_KEY: getattr(settings, ANALYTICS_KEY, None)}
