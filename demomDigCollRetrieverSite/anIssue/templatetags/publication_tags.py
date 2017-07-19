from django import template
from anIssue.models import APublication

register = template.Library()

@register.inclusion_tag('anissue/tags/publications.html', takes_context=True)
def publications(context):
    return {
        'publications': APublication.objects.all(),
        'request': context['request'],
    }
