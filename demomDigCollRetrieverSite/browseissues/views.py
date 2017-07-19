from django.shortcuts import render

from anIssue.models import AnIssuePage

# Create your views here.

def browse_issues_by_publication(request):
    results = ["test1", "test2", "test3"]
    print(AnIssuePage.objects.all())
    return render(request,
                  "browseissues/browse.html",
                  {'results': results})
