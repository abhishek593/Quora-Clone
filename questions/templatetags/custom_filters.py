from django import template


register = template.Library()


@register.filter(name='changeToInt')
def changeToInt(value):
    return int(value)
