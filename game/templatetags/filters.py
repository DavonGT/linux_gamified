from django import template

register = template.Library()

# Filter to get an attribute from an object
@register.filter
def get_attr(obj, attr_name):
    return getattr(obj, attr_name, '')  

# Filter to split a string into a list by a given delimiter
@register.filter
def split(value, delimiter):
    """Splits a string by the given delimiter and returns a list."""
    return value.split(delimiter)
