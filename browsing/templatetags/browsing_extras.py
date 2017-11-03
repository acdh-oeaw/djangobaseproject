from django import template
register = template.Library()


@register.inclusion_tag('browsing/tags/class_definition.html', takes_context=True)
def class_definition(context):
    values = {}
    try:
        values['class_name'] = context['class_name']
        values['docstring'] = context['docstring']
    except:
        pass
    return values


@register.inclusion_tag('browsing/tags/column_selector.html', takes_context=True)
def column_selector(context):
    try:
        return {'columns': context['togglable_colums']}
    except:
        return {'columns': None}
