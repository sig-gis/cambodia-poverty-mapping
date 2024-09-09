from django import template
from django.utils.translation import get_language

register = template.Library()

@register.simple_tag(takes_context=True)
def strip_lang_prefix(context):
    request = context['request']
    language = get_language()
    language_prefix = f'/{language}/'
    if request.path.startswith(language_prefix):
        # Remove the language prefix from the path
        return request.path[len(language_prefix)-1:]
    return request.path
