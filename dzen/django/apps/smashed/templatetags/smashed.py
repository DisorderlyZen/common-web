from collections import OrderedDict
from django import template
from django.conf import settings
from django.template.context import Context
from django.template.defaultfilters import stringfilter

register = template.Library()

SMASH_CONTEXT_NAME = 'smashed_scripts'
SMASH_CONTEXT_API_KEY = 'smashed_scripts_api_key'

@register.filter
@stringfilter
def strip_blank_lines(value):
    return '\n'.join([line for line in value.split('\n') if line.strip()])

@register.simple_tag(takes_context=True)
def smash_local(context, url):
    url = '%s%s' % (settings.STATIC_URL, url.lstrip('/'))
    return smash_context(object(), context, url)

@register.simple_tag(takes_context=True)
def smash_remote(context, url):
    return smash_context(object(), context, url)

def smash_context(self, context, script_url):
    if SMASH_CONTEXT_NAME not in context.render_context:
        context.render_context[SMASH_CONTEXT_NAME] = [OrderedDict()]

    smash_context = context.render_context[SMASH_CONTEXT_NAME][-1]

    if self not in smash_context:
        smash_context[self] = []

    smash_context[self].append(script_url)

    return ''

@register.simple_tag(takes_context=True)
def smash_flush(context):
    context.render_context[SMASH_CONTEXT_NAME].append(OrderedDict())
    return ''

@register.simple_tag(takes_context=True)
def smash_key(context, api_key):
    context.render_context[SMASH_CONTEXT_API_KEY] = api_key
    return ''

@register.simple_tag(takes_context=True)
def smash_render(context, var_name=None):
    t = template.loader.get_template('smashed/client.html')
    rendered_template = t.render(Context(render_context(context, var_name)))

    if var_name:
        context[var_name] = rendered_template
        return ''

    return rendered_template

def render_context(context, var_name):
    def resource_list(resources):
        return [script for key in resources for script in resources[key]]

    smash_context = context.render_context.get(SMASH_CONTEXT_NAME, [])
    resource_set = [resource_list(resources) for resources in smash_context]

    api_key = context.render_context.get(SMASH_CONTEXT_API_KEY, getattr(settings, 'WESUMO_APP_KEY', None))

    if not api_key:
        debug = True
    elif var_name:
        debug = False
    else:
        debug = getattr(settings, 'DEBUG', False)

    return {
            'api_key': api_key,
            'debug': debug,
            'resource_set': resource_set
            }
