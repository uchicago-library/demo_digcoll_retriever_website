from django.core.management.base import BaseCommand
import json
from urllib.request import urlopen, Request
from xml.etree import ElementTree

from anIssue.models import AnIssuePage, Publication
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
            print(mdata_url)
            mdata_req = Request(mdata_url)
            mdata_data = None
            with urlopen(mdata_req) as response:
                if response.code == 200:
                    mdata_data = response.read()
                    print(mdata_data)

            d = ElementTree.fromstring(mdata_data)
            identifier = n_item["identifier"]
            title = d.find('title').text
            description = d.find('description').text
            date = d.find('date').text
            publication_check = Publication.objects.filter(publication_title=title)
            if publication_check.count() == 0:
                publication = Publication()
                publication.title = title
                publication.description = description
                publication.type = 'university'
            else:
                publication = publication_check[0]
            volume = identifier.split('-')[2]
            issue = identifier.split('-')[3]
            new_issue = AnIssuePage()
            new_issue.issue_publication = publication
            new_issue.volume = volume.lstrip('0')
            new_issue.issue = issue.lstrip('0')
            new_issue.title = title + 'volume ' + volume.lstrip('0') + ' issue ' + issue.lstrip('0')
            struct_url = options["digcoll_retriever_host"] + "/" + n_item["identifier"] + "/struct"
            home.add_child(instance=new_issue)
            for p in n_item["pages"]:
                page_url = options["digcoll_retriever_host"] + p + "/jpg"
                page_req = Request(page_url)
                with urlopen(page_req) as response:
                    if response.code == 200:
                        new_issue.issue_pages.create(page_url=page_url, page_number=p.split('_')[1].strip('.jpg'))
                        new_issue.save()
