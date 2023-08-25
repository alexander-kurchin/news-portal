from django import template


register = template.Library()


@register.simple_tag()
def header(title='Привет!'):
    section = f'<section class="category-section"><div class="container" data-aos="fade-up"><div class="section-header d-flex justify-content-between align-items-center mb-5"><h1>{title}</h1></div></div></section>'
    return section
