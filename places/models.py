import re
from django.db import models
from django.core.urlresolvers import reverse
from idprovider.models import IdProvider


class AlternativeName(IdProvider):
    name = models.CharField(max_length=250, blank=True, help_text="Alternative Name")

    def get_absolute_url(self):
        return reverse('places:alternativename_detail', kwargs={'pk': self.id})

    @classmethod
    def get_listview_url(self):
        return reverse('places:alternativename_list')

    @classmethod
    def get_createview_url(self):
        return reverse('places:alternativename_create')

    def get_next(self):
        next = AlternativeName.objects.filter(id__gt=self.id)
        if next:
            return next.first().id
        return False

    def get_prev(self):
        prev = AlternativeName.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return prev.first().id
        return False

    def get_absolute_url(self):
        return reverse('places:alternativename_detail', kwargs={'pk': self.id})

    def __str__(self):
        return "{}".format(self.name)


class Place(IdProvider):
    PLACE_TYPES = (
        ("city", "city"),
        ("country", "country")
    )

    """Holds information about places."""
    name = models.CharField(
        max_length=250, blank=True, help_text="Normalized name"
    )
    alternative_name = models.ManyToManyField(
        AlternativeName,
        max_length=250, blank=True,
        help_text="Alternative names"
    )
    geonames_id = models.CharField(
        max_length=50, blank=True,
        help_text="GND-ID"
    )
    lat = models.DecimalField(
        max_digits=20, decimal_places=12,
        blank=True, null=True
    )
    lng = models.DecimalField(
        max_digits=20, decimal_places=12, blank=True, null=True
    )
    part_of = models.ForeignKey(
        "Place", null=True, blank=True,
        help_text="A place (country) this place is part of.",
        related_name="has_child"
    )
    place_type = models.CharField(choices=PLACE_TYPES, null=True, blank=True, max_length=50)

    def get_geonames_url(self):
        if self.geonames_id.startswith('ht') and self.geonames_id.endswith('.html'):
            return self.geonames_id
        else:
            return "http://www.geonames.org/{}".format(self.geonames_id)

    def get_geonames_rdf(self):
        try:
            number = re.findall(r'\d+', str(self.geonames_id))[0]
            return None
        except:
            return None

    @classmethod
    def get_listview_url(self):
        return reverse('browsing:browse_places')

    @classmethod
    def get_createview_url(self):
        return reverse('places:place_create')

    @classmethod
    def get_arche_dump(self):
        return reverse('browsing:rdf_places')

    def get_next(self):
        next = Place.objects.filter(id__gt=self.id)
        if next:
            return next.first().id
        return False

    def get_prev(self):
        prev = Place.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return prev.first().id
        return False

    def get_absolute_url(self):
        return reverse('places:place_detail', kwargs={'pk': self.id})

    def __str__(self):
        return "{}".format(self.name)


class Institution(IdProvider):
    legacy_id = models.CharField(max_length=300, blank=True)
    written_name = models.CharField(max_length=300, blank=True)
    authority_url = models.CharField(max_length=300, blank=True)
    alt_names = models.CharField(max_length=300, blank=True)
    abbreviation = models.CharField(max_length=300, blank=True)
    location = models.ForeignKey(Place, blank=True, null=True)
    parent_institution = models.ForeignKey(
        'Institution', blank=True, null=True, related_name='children_institutions')
    comment = models.TextField(blank=True)

    @classmethod
    def get_arche_dump(self):
        return reverse('browsing:rdf_institutions')

    @classmethod
    def get_listview_url(self):
        return reverse('browsing:browse_institutions')

    @classmethod
    def get_createview_url(self):
        return reverse('places:institution_create')

    def get_absolute_url(self):
        return reverse('places:institution_detail', kwargs={'pk': self.id})

    def get_next(self):
        next = Institution.objects.filter(id__gt=self.id)
        if next:
            return next.first().id
        return False

    def get_prev(self):
        prev = Institution.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return prev.first().id
        return False

    def __str__(self):
        return "{}".format(self.written_name)


class Person(IdProvider):
    legacy_id = models.CharField(max_length=300, blank=True)
    written_name = models.CharField(max_length=300, blank=True)
    forename = models.CharField(max_length=300, blank=True)
    name = models.CharField(max_length=300, blank=True)
    acad_title = models.CharField(max_length=300, blank=True)
    alt_names = models.CharField(max_length=300, blank=True)
    belongs_to_institution = models.ForeignKey(
        Institution, blank=True, null=True, related_name="has_member"
    )
    authority_url = models.CharField(max_length=300, blank=True)
    comment = models.TextField(blank=True)

    @classmethod
    def get_createview_url(self):
        return reverse('places:person_create')

    @classmethod
    def get_listview_url(self):
        return reverse('browsing:browse_persons')

    @classmethod
    def get_arche_dump(self):
        return reverse('browsing:rdf_persons')

    def get_absolute_url(self):
        return reverse('places:person_detail', kwargs={'pk': self.id})

    def get_next(self):
        next = Person.objects.filter(id__gt=self.id)
        if next:
            return next.first().id
        return False

    def get_prev(self):
        prev = Person.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return prev.first().id
        return False

    def __str__(self):
        return "{}".format(self.written_name)
