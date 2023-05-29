from django import template

register = template.Library()

@register.filter
def removetag(querydict, tag):
    querydict = querydict.copy()
    querydict.pop(tag, None)
    return querydict.urlencode()

@register.filter
def trange(num):
    num = int(num)
    list = []
    for i in range(num):
        list.append(1)
    return list
