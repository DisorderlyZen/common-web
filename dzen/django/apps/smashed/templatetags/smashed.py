from collections import OrderedDict
from django import template

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
        block_context = context.get('block')

        if block_context not in smash_context:
            smash_context[block_context] = []

        smash_context[block_context].append(self.script_url)

        return ''

@register.inclusion_tag('smashed_client.html', takes_context=True)
def smash_render(context):
        smash_context = context.render_context.get(SMASH_CONTEXT_NAME, {})
        return {
                'api_key': '1234',
                'resource_list': ','.join([script for key in reversed(smash_context) for script in smash_context[key]])
    

#class SmashRenderNode(template.Node):
#    def render(self, context):
#        smash_context = context.render_context.get(SMASH_CONTEXT_NAME, {})
#        return ','.join([script for key in reversed(smash_context) for script in smash_context[key]])