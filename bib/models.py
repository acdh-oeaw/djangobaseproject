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
            return "/".join([settings.Z_BASE_URL, settings.Z_COLLECTION, 'itemKey', self.zoterokey])
        except:
            return None

    def __str__(self):
        return "{}, {}".format(self.author, self.title)
