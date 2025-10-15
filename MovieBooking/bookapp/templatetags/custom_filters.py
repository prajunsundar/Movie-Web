from django import template
register = template.Library()

@register.filter
def pluck(queryset, key):
    return [obj[key] for obj in queryset]