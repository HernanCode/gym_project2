from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_id(dictionary,key):
    obj = get_item(dictionary, key)
    return obj.id if obj else None