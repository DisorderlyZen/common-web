from collections import OrderedDict
from django import template
from django.conf import settings
from django.template.context import Context
from django.template.defaultfilters import stringfilter

register = template.Library()

SMASH_CONTEXT_STYLE = 'smashed_context:style'
SMASH_CONTEXT_SCRIPT = 'smashed_context:script'
SMASH_CONTEXT_API_KEY = 'smashed_context:api_key'

@register.simple_tag(takes_context=True)
def smash_local_style(context, url):
    return smash_local_resource(context, url, SMASH_CONTEXT_STYLE)

@register.simple_tag(takes_context=True)
def smash_remote_style(context, url):
    return smash_remote_resource(context, url, SMASH_CONTEXT_STYLE)

@register.simple_tag(takes_context=True)
def smash_local_script(context, url):
    return smash_local_resource(context, url, SMASH_CONTEXT_SCRIPT)

@register.simple_tag(takes_context=True)
def smash_remote_script(context, url):
    return smash_remote_resource(context, url, SMASH_CONTEXT_SCRIPT)

def smash_local_resource(context, url, context_name):
    url = settings.STATIC_URL + url.lstrip('/')
    return smash_remote_resource(context, url, context_name)

def smash_remote_resource(context, url, context_name):
    return smash_context(object(), context, url, context_name)

@register.filter
@stringfilter
def strip_blank_lines(value):
    return '\n'.join([line for line in value.split('\n') if line.strip()])

def smash_context(self, context, url, context_name):
    if context_name not in context.render_context:
        context.render_context[context_name] = [OrderedDict()]

    smash_context = context.render_context[context_name][-1]

    if self not in smash_context:
        smash_context[self] = []

    smash_context[self].append(url)

    return ''

@register.simple_tag(takes_context=True)
def smash_flush_styles(context):
    return smash_flush(context, SMASH_CONTEXT_STYLE)

@register.simple_tag(takes_context=True)
def smash_flush_scripts(context):
    return smash_flush(context, SMASH_CONTEXT_SCRIPT)

def smash_flush(context, context_name):
    context.render_context[context_name].append(OrderedDict())
    return ''

@register.simple_tag(takes_context=True)
def smash_key(context, api_key):
    context.render_context[SMASH_CONTEXT_API_KEY] = api_key
    return ''

@register.simple_tag(takes_context=True)
def smash_render_scripts(context, var_name=None):
    return smash_render_resources(context, var_name, 'smashed/scripts.html', SMASH_CONTEXT_SCRIPT)

@register.simple_tag(takes_context=True)
def smash_render_styles(context, var_name=None):
    return smash_render_resources(context, var_name, 'smashed/styles.html', SMASH_CONTEXT_STYLE)

def smash_render_resources(context, var_name, template_name, context_name):
    t = template.loader.get_template(template_name)
    rendered_template = t.render(render_context(context, var_name, context_name))

    if var_name:
        context[var_name] = rendered_template
        return ''

    return rendered_template

def render_context(context, var_name, context_name):
    def resource_list(resources):
        return [script for key in resources for script in resources[key]]

    smash_context = context.render_context.get(context_name, [])
    resource_set = [resource_list(resources) for resources in smash_context]

    api_key = context.render_context.get(SMASH_CONTEXT_API_KEY, getattr(settings, 'WESUMO_APP_KEY', None))

    if not api_key:
        debug = True
    elif var_name:
        debug = False
    else:
        debug = getattr(settings, 'DEBUG', False)

    return Context({
            'api_key': api_key,
            'debug': debug,
            'resource_set': resource_set
            })
