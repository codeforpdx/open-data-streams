from django import template

register = template.Library()

@register.inclusion_tag('nav_item.html')
def nav_item(request, url, title):
    active = url == request.get_full_path()
    return {'url': url, 'title': title, 'active': active}
