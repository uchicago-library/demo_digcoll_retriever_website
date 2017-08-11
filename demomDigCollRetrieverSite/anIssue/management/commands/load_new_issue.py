
from xml.etree import ElementTree
from sys import stdout
from urllib.request import urlopen, Request
import json
from django.core.management.base import BaseCommand
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
                            help="The host of the digcoll_retriever", type=str),
        parser.add_argument("import_data_file",
                            help="An identifier for a particular MVol issue", type=str)
        parser.add_argument("project_api_host",
                            help="Enter the host that the project api is on", type=str)

    def handle(self, *args, **options):
        data = json.load(open(options["import_data_file"], 'r', encoding='utf-8'))
        home = Page.objects.filter(title='Home')[0]
        project_host = options["project_api_host"]
        for n_item in data:
            metadata_url = options["digcoll_retriever_host"] + n_item["metadata"]
            metadata_req = Request(metadata_url)
            metadata_data = None
            ocr_data_url = project_host + n_item["identifier"] + "/ocr?jpg_height=1000&jpg_width=1000"
            ocr_data = None
            with urlopen(metadata_req) as response:
                if response.code == 200:
                    metadata_data = response.read()
            with urlopen(ocr_data_url) as response:
                if response.code == 200:
                    ocr_data = response.read()
            xml_data = ElementTree.fromstring(metadata_data)
            identifier = n_item["identifier"]
            title = xml_data.find('title').text
            description = xml_data.find('description').text
            date = xml_data.find('date').text
            publication_check = Publication.objects.filter(publication_title=title)
            if publication_check.count() == 0:
                publication = Publication()
                publication.publication_title = title
                publication.publication_description = description
                publication_type = PublicationType.objects.filter(publication_type='University')[0]
                publication.the_type = publication_type
                publication.save()
            else:
                publication = publication_check[0]
            volume = identifier.split('-')[2]
            issue = identifier.split('-')[3]
            issue_str = issue.lstrip('0') if issue.lstrip('0') != "" else '0'
            the_title = title + ' volume ' + volume.lstrip('0') + ' issue ' + issue_str
            if AnIssuePage.objects.filter(title=the_title).count() == 0:
                new_issue = AnIssuePage()
                new_issue.ocr_document = ocr_data
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
                purl = options["digcoll_retriever_host"] + p + "/jpg"
                current_urls = [x.page_url
                                for x in issue_page.issue_pages.all() if x.page_url==purl]
                if len(current_urls) == 0:
                    issue_page.issue_pages.create(page_url=purl,
                                                  page_number=p.split('_')[1].strip('.jpg'))
                    issue_page.save()
                    stdout.write("{} has been added to the issue {} in the website.\n".format(p, the_title))
            stdout.write("{} has been saved to the website.\n".format(n_item["identifier"]))
        stdout.write("finished processing {}.\n".format(options["import_data_file"]))