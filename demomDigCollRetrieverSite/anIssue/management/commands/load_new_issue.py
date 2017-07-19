from django.core.management.base import BaseCommand
from urllib.request import urlopen, Request

from anIssue.models import AnIssuePage

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
        parser.add_argument("new_identifier",
                            help="An identifier for a particular MVol issue", type=str)


    def handle(self, *args, **options):
        url_path = options["digcoll_retriever_host"].strip() + options["new_identifier"].strip() + "/stat"
        print(url_path)
        req = Request(url_path)
        with urlopen(req) as response:
            print(response.code)