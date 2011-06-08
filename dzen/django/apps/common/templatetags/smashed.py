from django import template

register = template.library()

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
            context.render_context[SMASH_CONTEXT_NAME] = []

        context.render_context[SMASH_CONTEXT_NAME].append(script_url)
        return ''

@register.tag
def smash_render(parser, token):
    return SmashRenderNode()

class SmashRenderNode(template.Node):
    def render(self, context):
        if SMASH_CONTEXT_NAME not in context.render_context:
            return ''

        return ','.join(context.render_context[SMASH_CONTEXT_NAME])
