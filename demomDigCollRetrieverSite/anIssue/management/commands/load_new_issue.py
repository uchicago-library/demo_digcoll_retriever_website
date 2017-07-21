from django.core.management.base import BaseCommand
import json
from urllib.request import urlopen, Request
from xml.etree import ElementTree

from anIssue.models import AnIssuePage, Publication, PublicationType
from wagtail.wagtailcore.models import Page

class Command(BaseCommand):
    """a management command to retrieve catalog item data and write it to a CSV file

    This class is necessary for generating a CSV file that can be audited.
    """

    help = "A management command to export data from catalogitems into a CSV file"

    def add_arguments(self, parser):
        """the method that gets called to add parameter to the management command

        It takes a parser object and adds a string type argument called
        legacy_data_filepath
        """
        parser.add_argument("digcoll_retriever_host",
                            help="The host of the digcoll_retriever"),
        parser.add_argument("import_data_file",
                            help="An identifier for a particular MVol issue", type=str)


    def handle(self, *args, **options):
        data = json.load(open(options["import_data_file"], 'r', encoding='utf-8'))
        home = Page.objects.filter(title='Home')[0]

        for n_item in data:
            mdata_url = options["digcoll_retriever_host"] + n_item["metadata"]
            mdata_req = Request(mdata_url)
            mdata_data = None
            with urlopen(mdata_req) as response:
                if response.code == 200:
                    mdata_data = response.read()
            d = ElementTree.fromstring(mdata_data)
            identifier = n_item["identifier"]
            title = d.find('title').text
            description = d.find('description').text
            date = d.find('date').text
            publication_check = Publication.objects.filter(publication_title=title)
            print(publication_check)
            if publication_check.count() == 0:
                publication = Publication()
                publication.publication_title = title
                publication.publication_description = description
                ptype = PublicationType.objects.filter(publication_type='University')[0]
                print(ptype)
                publication.the_type = ptype
                publication.save()
            else:
                publication = publication_check[0]
            volume = identifier.split('-')[2]
            issue = identifier.split('-')[3] 
            issue_str = issue.lstrip('0') if issue.lstrip('0') != "" else '0'
            the_title = title + ' volume ' + volume.lstrip('0') + ' issue ' + issue_str
            if AnIssuePage.objects.filter(title=the_title).count() == 0:
                new_issue = AnIssuePage()
                new_issue.issue_publication = publication
                new_issue.volume = volume.lstrip('0')
                new_issue.issue = issue.lstrip('0') if issue.lstrip('0') != '' else '0'
                new_issue.title = the_title 
                new_issue.publication_date = date
                new_issue.identifier = identifier
                home.add_child(instance=new_issue)
                issue_page = AnIssuePage.objects.filter(title=the_title)[0]
            else:
                issue_page = AnIssuePage.objects.filter(title=the_title)[0]
            for p in n_item["pages"]:
                page_url = options["digcoll_retriever_host"] + p + "/jpg"
                issue_page.issue_pages.create(page_url=page_url, page_number=p.split('_')[1].strip('.jpg'))
                issue_page.save()