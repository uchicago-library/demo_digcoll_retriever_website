from django import template
from anIssue.models import Publication

register = template.Library()

@register.inclusion_tag('anissue/tags/publications.html', takes_context=True)
def publications(context):
    return {
        'publications': Publication.objects.all(),
        'request': context['request'],
    }
