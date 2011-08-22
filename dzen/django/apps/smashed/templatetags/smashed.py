from collections import OrderedDict
from django import template
from django.conf import settings
from django.template.context import RequestContext
from django.template.defaultfilters import escapejs

register = template.Library()

SMASH_CONTEXT_NAME = 'smashed_scripts'

@register.tag
def smash_local(parser, token):
    script_url = smash_parse(parser, token)
    return SmashAddNode('%s%s' % (settings.STATIC_URL, script_url.lstrip('/')))

@register.tag
def smash_remote(parser, token):
    return SmashAddNode(smash_parse(parser, token))

def smash_parse(parser, token):
    try:
        tag_name, script_url = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('%r tag requires arguments' % token.contents.split()[0])

    return script_url

class SmashAddNode(template.Node):
    def __init__(self, script_url):
        self.script_url = script_url

    def render(self, context):
        if SMASH_CONTEXT_NAME not in context.render_context:
            context.render_context[SMASH_CONTEXT_NAME] = [OrderedDict()]

        smash_context = context.render_context[SMASH_CONTEXT_NAME][-1]

        if self not in smash_context:
            smash_context[self] = []

        smash_context[self].append(self.script_url)

        return ''

@register.tag
def smash_flush(parser, token):
    return SmashFlushNode()

class SmashFlushNode(template.Node):
    def render(self, context):
        context.render_context[SMASH_CONTEXT_NAME].append(OrderedDict())
        return ''

@register.inclusion_tag('smashed/client.html', takes_context=True)
def smash_render(context):
    def resource_list(resources):
        return [script for key in resources for script in resources[key]]

    smash_context = context.render_context.get(SMASH_CONTEXT_NAME, [])
    resource_set = [resource_list(resources) for resources in smash_context]

    return RequestContext(context['request'], {
            'api_key': getattr(settings, 'WESUMO_APP_KEY', None),
            'resource_set': resource_set
            })
