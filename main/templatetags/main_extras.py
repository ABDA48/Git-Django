from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, [])

@register.filter
def get_keys(dictionary):
    return list(dictionary.keys())

@register.filter
def get_values(dictionary):
    return list(dictionary.values()) 