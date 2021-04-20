from django.template.defaulttags import register
from logging import warning
@register.filter
def get_item(dictionary, key):
    value = ''
    if isinstance(dictionary, dict):
        if dictionary.get(key):
            value = dictionary.get(key)
    return value

@register.filter
def get_object_item(object_item, key):
    value = ''
    if key in object_item.__dir__():
        value = getattr(object_item, key)
    elif isinstance(object_item, dict):
        if object_item.get(key):
            value = object_item.get(key)
    return value
