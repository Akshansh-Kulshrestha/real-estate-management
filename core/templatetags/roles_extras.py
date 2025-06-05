from django import template

register = template.Library()

@register.filter(name='has_role')
def has_role(user, role_name):
    return user.has_role(role_name)
