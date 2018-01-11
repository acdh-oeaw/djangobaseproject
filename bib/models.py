# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings


class Book(models.Model):
    zoterokey = models.CharField(max_length=100, primary_key=True)
    item_type = models.CharField(max_length=100, blank=True, null=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=500, blank=True, null=True)
    publication_title = models.CharField(max_length=100, blank=True, null=True)
    short_title = models.CharField(max_length=500, blank=True, null=True)
    publication_year = models.IntegerField(blank=True, null=True)
    place = models.CharField(max_length=100, blank=True, null=True)
    isbn = models.CharField(max_length=100, blank=True, null=True)
    issn = models.CharField(max_length=100, blank=True, null=True)
    doi = models.CharField(max_length=100, blank=True, null=True)
    url = models.CharField(max_length=100, blank=True, null=True)

    def get_zotero_url(self):
        "Returns the objects URL pointing to its Zotero entry"
        try:
            base = "https://www.zotero.org/{}/".format(settings.Z_ID_TYPE)
            url = "{}{}/peter_handke_stage_texts/items/itemKey/{}".format(
                base, settings.Z_ID, self.zoterokey
            )
            return url
        except AttributeError:
            return "please provide Zotero settings"

    def __str__(self):
        return "{}, {}".format(self.author, self.title)
