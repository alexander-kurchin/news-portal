from django import template


register = template.Library()


@register.simple_tag()
def header(title='Привет!'):
    """Создаёт красивый заголовок h1"""

    section = f'<section class="category-section"><div class="container"><div class="section-header d-flex justify-content-between align-items-center mb-5"><h1>{title}</h1></div></div></section>'
    return section


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    """Позволяет не терять текущие параметры запроса"""

    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()
