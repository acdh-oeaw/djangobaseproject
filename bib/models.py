# -*- coding: utf-8 -*-
from django.urls import reverse
from django.db import models
from django.conf import settings


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
    zot_version = models.CharField(
        blank=True, verbose_name="version", max_length=50,
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
        return "{}".format(self.zot_key)


class Book(models.Model):
    zoterokey = models.CharField(max_length=500, primary_key=True)
    item_type = models.CharField(max_length=500, blank=True, null=True)
    author = models.CharField(max_length=500, blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    publication_title = models.CharField(max_length=500, blank=True, null=True)
    short_title = models.CharField(max_length=500, blank=True, null=True)
    publication_year = models.IntegerField(blank=True, null=True)
    place = models.CharField(max_length=500, blank=True, null=True)
    isbn = models.CharField(max_length=500, blank=True, null=True)
    issn = models.CharField(max_length=500, blank=True, null=True)
    doi = models.CharField(max_length=500, blank=True, null=True)
    url = models.CharField(max_length=500, blank=True, null=True)

    def get_zotero_url(self):
        "Returns the objects URL pointing to its Zotero entry"
        try:
            base = "https://www.zotero.org/{}/".format(settings.Z_ID_TYPE)
            url = "{}/items/itemKey/{}".format(
                settings.Z_COLLECTION_URL, self.zoterokey
            )
            return url
        except AttributeError:
            return "please provide Zotero settings"

    def __str__(self):
        return "{}, {}".format(self.author, self.title)


class Reference(models.Model):
    """Contains a precise bibliographic reference"""
    zotero_item = models.ForeignKey(
        Book, blank=True, null=True,
        verbose_name="Zotero Item",
        help_text="Select the zotero item you would like to quote",
        related_name="has_references",
        on_delete=models.SET_NULL
    )
    page = models.CharField(
        max_length=250, blank=True, null=True,
        verbose_name="Page Number",
        help_text="Page Number"
    )

    class Meta:
        ordering = ['-id']

    @classmethod
    def get_listview_url(self):
        return reverse('bib:browse_references')

    @classmethod
    def get_createview_url(self):
        return reverse('bib:reference_create')

    def get_next(self):
        next = Reference.objects.filter(id__gt=self.id)
        if next:
            return next.first().id
        return False

    def get_prev(self):
        prev = Reference.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return prev.first().id
        return False

    def get_absolute_url(self):
        return reverse(
            'bib:reference_detail', kwargs={'pk': self.id}
        )

    def __str__(self):
        try:
            return "{}, {}".format(self.zotero_item, self.page)
        except:
            return self.id
