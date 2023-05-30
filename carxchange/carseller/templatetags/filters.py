from django import template

register = template.Library()

@register.filter
def removetag(querydict, tag, second=None):
    querydict = querydict.copy()
    querydict.pop(tag, None)
    if second:
        querydict.pop(second, None)
    return querydict.urlencode()

@register.filter
def trange(num):
    num = int(num)
    list = []
    for i in range(num):
        list.append(1)
    return list

@register.filter
def removetags(query_string, tags):
    tag_list = [tag.strip() for tag in tags.split(',')]
    updated_query_dict = query_string.copy()
    
    for tag in tag_list:
        if tag in updated_query_dict:
            del updated_query_dict[tag]
    
    return updated_query_dict.urlencode()
