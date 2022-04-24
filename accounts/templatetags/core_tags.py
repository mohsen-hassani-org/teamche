from django import template
register = template.Library()

@register.filter
def multiply(x, y):
    return x * y

@register.filter
def mod(x, y):
    return x % y
