import os
import datetime
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from bib.zot_utils import items_to_dict, create_zotitem

library_id = settings.Z_ID
library_type = settings.Z_LIBRARY_TYPE
api_key = settings.Z_API_KEY


class Command(BaseCommand):

    """ Imports items from zotero-bib """

    help = "Imports all items from zotero-bib"

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            dest='limit',
            help="Max number of items to import"
        )
        parser.add_argument(
            '--since',
            dest='since',
            help="The version (string) from which on items should be imported"
        )

    def handle(self, *args, **options):
        if options['limit']:
            limit = int(options['limit'])
        else:
            limit = None
        if options['since']:
            since = options['since']
        else:
            since = None

        self.stdout.write(
            self.style.SUCCESS("{}, {}".format(limit, since))
        )
        self.stdout.write(
            self.style.SUCCESS("started: {}".format(datetime.datetime.now()))
        )
        items = items_to_dict(library_id, library_type, api_key, limit=limit, since_version=since)
        self.stdout.write(
            self.style.SUCCESS("fetched {} items".format(len(items['items'])))
        )
        self.stdout.write(
            self.style.SUCCESS("{}".format(datetime.datetime.now()))
        )
        self.stdout.write(
            self.style.SUCCESS('starting creating/updating models now')
        )
        for x in items['bibs']:
            temp_item = create_zotitem(x)
            self.stdout.write(
                self.style.SUCCESS('created: {}'.format(temp_item))
            )
        self.stdout.write(
            self.style.SUCCESS("ended: {}".format(datetime.datetime.now()))
        )
