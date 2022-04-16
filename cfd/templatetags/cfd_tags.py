from django import template
register = template.Library()

@register.filter
def classname(obj):
    return obj.__class__.__name__

@register.filter
def get_model_name(instance):
    return instance._meta.model_name
    
@register.filter
def ins(obj, cls):
    return isinstance(obj, cls)
