from django import template
from anissue.models import Publication

register = template.Library()

@register.inclusion_tags('anissue/tags/publications.html')
def publications(context):
    return {
        'publications': Publication.objects.all(),
        'request': context['request'],
    }