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
        print(data)
 