from django import template

register = template.Library()

@register.filter
def to_alpha(value):
    """Convert a number to its corresponding alphabet (1 -> a, 2 -> b, etc.)"""
    if value < 1:
        return ''
    return chr(96 + value)  # 97 is 'a' in ASCII

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

