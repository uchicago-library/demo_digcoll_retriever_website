from django.core.management.base import BaseCommand
import json
from urllib.request import urlopen, Request
from xml.etree import ElementTree
from sys import stdout, stderr

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
        parser.add_argument("project_api",
                            help="", type=str)
        parser.add_argument("import_data_file",
                            help="An identifier for a particular MVol issue", type=str)

    def handle(self, *args, **options):
        data = json.load(open(options["import_data_file"], 'r', encoding='utf-8'))
        issue_to_correct = data["identifier"]
        correction_to_make = data["correction"]
        if correction_to_make == "new metadata":
            # do work to update publication, volume, issue, publication date
            metadata_req = Request(data["correction_loc"])
            metadata_data = None
            with urlopen(metadata_req) as response:
                if response.code == 200:
                    metadata_data = response.read()
            xml_data = ElementTree.fromstring(metadata_data)
            new_title = xml_data.find('title').text
            new_description = xml_data.find('description').text
            new_date = xml_data.find('date').text
            issue_to_update = AnIssuePage.objects.filter(identifier=issue_to_correct)
            if issue_to_update.count() ==1:
                publication = issue_to_update[0].issue_publication
                publication.publication_title = new_title
                publication.publication_description = new_description
                issue_to = issue_to_update[0]
                issue_to.publication_date = new_date
                publication.save()
                issue_to.save()
        elif correction_to_make == "new files":
            # do work to add or delete a page
            ocr_data_url = options["project_api"] + data["identifier"] + "/ocr?jpg_height=1000&jpg_width=1000"
            ocr_data_req = Request(ocr_data_url)
            ocr_data = None
            the_issue_to_update =  AnIssuePage.objects.filter(identifier=data["identifier"])
            with urlopen(ocr_data_req) as response:
                if response.code == 200:
                    ocr_data = response.read()
            if the_issue_to_update.count() == 1:
                the_issue = the_issue_to_update[0]
                the_issue.ocr_document = ocr_data
                the_issue.save()