from django import template
register = template.Library()

@register.filter(name='includecss')
def includecss(field, className):
    return field.as_widget(attrs={"class":className})