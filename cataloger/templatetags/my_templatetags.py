from django import template

register = template.Library()

@register.inclusion_tag('nav_item.html')
def nav_item(url, title, curpath):
    return {'url': url, 'title': title, 'curpath': curpath}