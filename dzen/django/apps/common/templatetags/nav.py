from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def active_url(request, url, *args):
    if request.path == reverse(url, args=args):
        return 'active'
    return ''

@register.simple_tag
def active_url_prefix(request, url, *args):
    if request.path.startswith(reverse(url, args=args)):
        return 'active'
    return ''
