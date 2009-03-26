import os.path

from django.conf import settings
from django.template import Template, TemplateSyntaxError, TemplateDoesNotExist
from django.template import Library, Node
from django.template.loader import get_template
from django.template.loader_tags import BlockNode

register = Library()

class ExtendsNode(Node):
    def __init__(self, nodelist, ref_template, parent_name):
        self.nodelist = nodelist
        self.ref_template = ref_template
        self.parent_name = parent_name

    def get_parent(self, context):
        parent = self.parent_name
        if not parent:
            error_msg = "Invalid template name in 'extends' tag: %r." % parent
            raise TemplateSyntaxError, error_msg
        try:
            t = self.ref_template.resolve(context)
            if not isinstance(t, Template):
                raise TemplateSyntaxError, "The first argument to %r tag must be a Template instance" % bits[0]
            template_basedir = os.path.split(t.name)[0]
            template_path = os.path.join(template_basedir, self.parent_name)
            return get_template(template_path)
        except TemplateDoesNotExist:
            raise TemplateSyntaxError, "Template %r cannot be extended, because it doesn't exist" % parent

    def render(self, context):
        compiled_parent = self.get_parent(context)
        parent_is_child = isinstance(compiled_parent.nodelist[0], ExtendsNode)
        parent_blocks = dict([(n.name, n) for n in compiled_parent.nodelist.get_nodes_by_type(BlockNode)])
        for block_node in self.nodelist.get_nodes_by_type(BlockNode):
            # Check for a BlockNode with this node's name, and replace it if found.
            try:
                parent_block = parent_blocks[block_node.name]
            except KeyError:
                # This BlockNode wasn't found in the parent template, but the
                # parent block might be defined in the parent's *parent*, so we
                # add this BlockNode to the parent's ExtendsNode nodelist, so
                # it'll be checked when the parent node's render() is called.
                if parent_is_child:
                    compiled_parent.nodelist[0].nodelist.append(block_node)
            else:
                # Keep any existing parents and add a new one. Used by BlockNode.
                parent_block.parent = block_node.parent
                parent_block.add_parent(parent_block.nodelist)
                parent_block.nodelist = block_node.nodelist
        return compiled_parent.render(context)

class ConstantIncludeNode(Node):
    def __init__(self, ref_template, template_path):
        self.ref_template = ref_template
        self.template_path = template_path

    def render(self, context):
        try:
            t = self.ref_template.resolve(context)
            if not isinstance(t, Template):
                raise TemplateSyntaxError, "The first argument to %r tag must be a Template instance" % bits[0]
            template_basedir = os.path.split(t.name)[0]
            template_path = os.path.join(template_basedir, self.template_path)
            template = get_template(template_path)
            return template.render(context)
        except:
            if settings.TEMPLATE_DEBUG:
                raise
            return ''

def do_extends(parser, token):
    """
    Signal that this template extends a parent template.

    Example::

        {% fextends t "../base" %}

    t is a Template instance. The idea is that base would be relative
    pathed to t.
    """
    bits = token.contents.split()
    if len(bits) != 3:
        raise TemplateSyntaxError, "'%s' takes two arguments" % bits[0]
    parent_name = None
    t = parser.compile_filter(bits[1])
    path = bits[2]
    if path[0] in ('"', "'") and path[-1] == path[0]:
        parent_name = path[1:-1]
    else:
        raise TemplateSyntaxError, "The second argument to %r tag must be a relative path to the Template instance" % bits[0]
    nodelist = parser.parse()
    if nodelist.get_nodes_by_type(ExtendsNode):
        raise TemplateSyntaxError, "'%s' cannot appear more than once in the same template" % bits[0]
    return ExtendsNode(nodelist, t, parent_name)

def do_include(parser, token):
    """
    Loads a template and renders it with the current context.

    Example::

        {% finclude t "../some_include" %}

    t is a Template instance. The idea is that the include would be relative
    pathed to t.
    """
    bits = token.contents.split()
    if len(bits) != 3:
        raise TemplateSyntaxError, "%r tag takes two arguments: a Template instance and the name of the template to be included" % bits[0]
    t = parser.compile_filter(bits[1])
    path = bits[2]
    if path[0] in ('"', "'") and path[-1] == path[0]:
        return ConstantIncludeNode(t, path[1:-1])
    else:
        raise TemplateSyntaxError, "The second argument to %r tag must be a relative path to the Template instance" % bits[0]

register.tag('fextends', do_extends)
register.tag('finclude', do_include)