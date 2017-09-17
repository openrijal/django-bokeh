from django import template

register = template.Library()

@register.filter
def get_plot_id(value):
    import re

    pattern = re.compile('[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')

    return re.findall(pattern, value)[0]
