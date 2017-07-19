from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailsnippets.models import register_snippet

# Create your models here.

@register_snippet
class APublication(models.Model):
    publication_title = models.CharField(max_length=255)

    def __str__(self):
        return self.publication_title

class AnIssuePage(Page):
    volume = models.CharField(max_length=50)
    issue = models.CharField(max_length=50)
    pdf_file = models.URLField()
    issue_publication = models.ForeignKey('anIssue.APublication',
                                          null=True,
                                          blank=True,
                                          related_name='+',
                                          on_delete=models.SET_NULL,
                                         )


    content_panels = Page.content_panels + [
        FieldPanel("volume"),
        FieldPanel("issue"),
        SnippetChooserPanel("issue_publication"),
        FieldPanel("pdf_file"),
        InlinePanel("issue_pages", label="Pages for this Issue"),
    ]

class PageImageOrderable(Orderable):
    issue = ParentalKey(AnIssuePage, related_name='issue_pages')
    page_url = models.URLField()
    page_number = models.IntegerField()

