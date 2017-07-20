from django.shortcuts import render

from anIssue.models import Publication, AnIssuePage

# Create your views here.

def browse_issues_by_publication_type(request):
    publication_type = request.GET.get('publication_type')
    results = Publication.objects.filter(the_type__publication_type=publication_type)
    return render(request,
                  "browseissues/browse.html",
                  {'results': results}
                  )

def browse_for_dates(request):
    results = AnIssuePage.objects.live()
    date_dict = {}
    for n in results:
        n_date = n.publication_date
        print(date_dict)
        try:
            date_dict[n_date] += 1
        except:
            date_dict[n_date] = 1
    return render(request,
                  "browseissues/browse_dates.html",
                  {'results': date_dict}
                 )