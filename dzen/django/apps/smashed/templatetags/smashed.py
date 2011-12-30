from django import template
from django.conf import settings
from urlparse import urlparse

register = template.Library()

SMASH_STYLE_REL = 'stylesheet'
SMASH_SCRIPT_REL = 'javascript'

@register.simple_tag
def smash_script(url):
    return smash_resource(url, SMASH_SCRIPT_REL)

@register.simple_tag
def smash_style(url):
    return smash_resource(url, SMASH_STYLE_REL)

@register.simple_tag
def smash_render(api_key, rel_type):
    smash_url = getattr(settings, 'SMASH_CLIENT_URL', settings.STATIC_URL+'js/smash.js')
    script_tag = '<script type="text/javascript" src="{}#key={}&type={}"></script>'
    return script_tag.format(smash_url, api_key, rel_type)

def smash_resource(url, rel_type):
    if is_relative_url(url):
        url = settings.STATIC_URL + url.lstrip('/')

    return build_smash_tag(url, rel_type)

def is_relative_url(url):
    return not urlparse(url).netloc

def build_smash_tag(url, rel_type):
    return '<link rel="{}/wesumo" href="{}" />'.format(rel_type, url)
