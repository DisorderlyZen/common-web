from collections import OrderedDict
from django import template
from django.template.defaultfilters import escapejs

register = template.Library()

SMASH_CONTEXT_NAME = 'smashed_scripts'

@register.tag
def smash_add(parser, token):
    try:
        tag_name, script_url = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('%r tag requires arguments' % token.contents.split()[0])

    return SmashAddNode(script_url)

class SmashAddNode(template.Node):
    def __init__(self, script_url):
        self.script_url = script_url

    def render(self, context):
        if SMASH_CONTEXT_NAME not in context.render_context:
            context.render_context[SMASH_CONTEXT_NAME] = OrderedDict()

        smash_context = context.render_context[SMASH_CONTEXT_NAME]

        if self not in smash_context:
            smash_context[self] = []

        smash_context[self].append(self.script_url)

        return ''

@register.inclusion_tag('smashed_client.html', takes_context=True)
def smash_render(context):
    smash_context = context.render_context.get(SMASH_CONTEXT_NAME, OrderedDict())
    resources = [script for key in smash_context for script in smash_context[key]]
    return {
            'api_key': '1234',
            'resources': resources
            }
