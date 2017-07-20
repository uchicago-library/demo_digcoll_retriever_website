from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailcore.fields import RichTextField

# Create your models here.

@register_snippet
class PublicationType(models.Model):
    publication_type = models.CharField(max_length=255)

    def __str__(self):
        return self.publication_type

@register_snippet
class Publication(models.Model):
    publication_title = models.CharField(max_length=255)
    publication_description = RichTextField()
    the_type = models.ForeignKey('anIssue.PublicationType',
                                 null=True,
                                 blank=True,
                                 related_name='+',
                                 on_delete=models.SET_NULL)

    def __str__(self):
        return self.publication_title

class AnIssuePage(Page):
    issue_publication = models.ForeignKey('anIssue.Publication',
                                          null=True,
                                          blank=True,
                                          related_name='+',
                                          on_delete=models.SET_NULL,
                                         )
    volume = models.CharField(max_length=50, blank=True, null=True)
    issue = models.CharField(max_length=50, blank=True, null=True)
    identifier = models.CharField(max_length=50)
    publication_date = models.CharField(max_length=255)

    content_panels = Page.content_panels + [
        FieldPanel("volume"),
        FieldPanel("issue"),
        FieldPanel("identifier"),
        FieldPanel("publication_date"),
        SnippetChooserPanel("issue_publication"),
        InlinePanel("issue_pages", label="Pages for this Issue"),
    ]

class PageImageOrderable(Orderable):
    issue = ParentalKey(AnIssuePage, related_name='issue_pages')
    page_url = models.URLField()
    page_number = models.IntegerField()

