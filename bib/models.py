# -*- coding: utf-8 -*-
from django.urls import reverse
from django.db import models
from django.conf import settings

from pyzotero import zotero

library_id = settings.Z_ID
library_type = settings.Z_LIBRARY_TYPE
api_key = settings.Z_API_KEY


def fetch_bibtex(zot_key):
    """ fetches the bibtex dict of the passed in key """
    result = {}
    zot = zotero.Zotero(library_id, library_type, api_key)
    try:
        result['bibtex'] = zot.item(zot_key, format='bibtex').entries_dict
        result['error'] = None
    except Exception as e:
        result['bibtex'] = None
        result['error'] = "{}".format(e)

    return result


class ZotItem(models.Model):

    """ Stores main bibliographic information of a Zotero Item """

    zot_key = models.CharField(
        max_length=20, primary_key=True, verbose_name='key',
        help_text="The Zotero Item Key"
    )
    zot_creator = models.TextField(
        blank=True, verbose_name="creators",
        help_text="Stores all information from zoteros 'creators' field."
    )
    zot_date = models.TextField(
        blank=True, verbose_name="date",
        help_text="Stores all information from zoteros 'date' field."
    )
    zot_item_type = models.TextField(
        blank=True, verbose_name="itemType",
        help_text="Stores all information from zoteros 'itemType' field."
    )
    zot_title = models.TextField(
        blank=True, verbose_name="title",
        help_text="Stores all information from zoteros 'title' field."
    )
    zot_pub_title = models.TextField(
        blank=True, verbose_name="publicationTitle",
        help_text="Stores all information from zoteros 'publicationTitle' field."
    )
    date_modified = models.DateTimeField(
        blank=True, null=True, verbose_name="dateModified",
        help_text="Stores all information from zoteros 'publicationTitle' field."
    )
    zot_pages = models.TextField(
        blank=True, verbose_name="pages",
        help_text="Stores all information from zoteros 'pages' field."
    )
    zot_version = models.IntegerField(
        blank=True, null=True, verbose_name="version",
        help_text="Stores all information from zoteros 'pages' field."
    )
    zot_html_link = models.CharField(
        blank=True, verbose_name="selflink html", max_length=500,
        help_text="Stores all information from zoteros 'selflink' field."
    )
    zot_api_link = models.CharField(
        blank=True, verbose_name="selflink api", max_length=500,
        help_text="Stores all information from zoteros self api link field."
    )
    zot_bibtex = models.TextField(
        blank=True, verbose_name="bibtex",
        help_text="Stores the item's bibtex representation."
    )

    class Meta:
        ordering = ['-zot_version']

    def __str__(self):
        if self.zot_bibtex:
            return "{}".format(self.zot_bibtex)
        else:
            return "{}: {}; {}".format(self.zot_creator, self.zot_title, self.zot_pub_title)

    def save(self, get_bibtex=False, *args, **kwargs):
        if get_bibtex:
            bibtex = fetch_bibtex(self.zot_key)
            if bibtex['bibtex']:
                self.zot_bibtex = "{}".format(bibtex['bibtex'])
                self.save()
            else:
                pass
            super(ZotItem, self).save(*args, **kwargs)
        else:
            super(ZotItem, self).save(*args, **kwargs)
