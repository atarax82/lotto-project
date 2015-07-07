from django import template
register = template.Library()

@register.filter('html_fieldtype')
def fieldtype(field):
    return field.field.widget.__class__.__name__[:-len('Input')].lower()
