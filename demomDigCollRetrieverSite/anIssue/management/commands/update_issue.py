from django.core.management.base import BaseCommand
import json
from urllib.request import urlopen, Request
from xml.etree import ElementTree
from sys import stdout

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
        issue_to_correct = data["identifier"]
        correction_to_make = data["correction"]
        if correction_to_make == "new metadata":
            # do work to update publication, volume, issue, publication date
            metadata_req = Request(metadata_url)
            metadata_data = None
            ocr_data_url = project_host + n_item["identifier"] + "/ocr?jpg_height=1000&jpg_width=1000"
            ocr_data = None
            with urlopen(metadata_req) as response:
                if response.code == 200:
                    metadata_data = response.read()
            xml_data = ElementTree.fromstring(metadata_data)
            title = xml_data.find('title').text
            description = xml_data.find('description').text
            date = xml_data.find('date').text
            publication_to_update = Publication.objects.filter(publication_title=title)
            the_issue_to_update =  AnIssuePage.objects.filter(title=the_title).count() == 0:

            title = xml_data.find('title').text
            description = xml_data.find('description').text
            date = xml_data.find('date').text

            if publication_to_update.count() == 1:
                publication = publication_to_update[0]
                publication.publication_title = title
                publication.publication_to_update
        elif correction_to_make == "new files":
            # do work to add or delete a page
            the_issue_to_update =  AnIssuePage.objects.filter(title=the_title).count() == 0:
            for p in data["new_files"]:
                purl = p["loc"]
                action = p["action"]
                if action == "addition":
                    issue_to_correct.issue_pages.update(page_url=purl, page_number=0)
                    issue_to_correct.save()
                    stdout.write("{} has been added to issue {}\n".format(purl, issue_to_correct))
                elif action == "subtraction":
                    stderr.out("subtraction not implemented")
