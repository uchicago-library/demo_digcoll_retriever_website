from __future__ import absolute_import, unicode_literals

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.shortcuts import render

from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch.models import Query

from anIssue.models import AnIssuePage

def search(request):
    search_query = request.GET.get('query', None)

    page = request.GET.get('page', 1)

    # Search
    if search_query:
        search_results = AnIssuePage.objects.all()
        query = Query.get(search_query)

        search_results = search_results.filter(Q(title__contains=search_query.strip()) |
                                               Q(ocr_document__contains=search_query.strip()))
        # Record hit
        query.add_hit()
    else:
        search_results = Page.objects.none()

    # Pagination
    paginator = Paginator(search_results, 10)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    return render(request, 'search/search.html', {
        'search_query': search_query,
        'search_results': search_results,
    })
