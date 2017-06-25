import os
from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.text import slugify


DEFAULT_PEFIX = os.path.basename(settings.BASE_DIR)

DEFAULT_NAMESPACE = "http://www.vocabs/{}/".format(DEFAULT_PEFIX)

LABEL_TYPES = (
    ('prefLabel', 'prefLabel'),
    ('altLabel', 'altLabel'),
    ('hiddenLabel', 'hiddenLabel'),
)

RELATION_TYPES = (
    ('narrower', 'narrower'),
    ('broader', 'broader'),
    ('related', 'related'),
    ('broadMatch', 'broadMatch'),
    ('relatedMatch', 'relatedMatch'),
    ('exactMatch', 'exactMatch'),
)


class SkosNamespace(models.Model):
    namespace = models.URLField(blank=True, default=DEFAULT_NAMESPACE)
    prefix = models.CharField(max_length=50, blank=True, default=DEFAULT_PEFIX)

    def __str__(self):
        return "{}".format(self.prefix)


class SkosConceptScheme(models.Model):
    dc_title = models.CharField(max_length=300, blank=True)
    namespace = models.ForeignKey(SkosNamespace, blank=True, null=True)
    dct_creator = models.URLField(blank=True)
    legacy_id = models.CharField(max_length=200, blank=True)

    def save(self, *args, **kwargs):
        if self.namespace is None:
            temp_namespace, _ = SkosNamespace.objects.get_or_create(
                namespace=DEFAULT_NAMESPACE, prefix=DEFAULT_PEFIX)
            temp_namespace.save()
            self.namespace = temp_namespace
        else:
            pass
        super(SkosConceptScheme, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('vocabs:skosconceptscheme_detail', kwargs={'pk': self.id})

    def __str__(self):
        return "{}:{}".format(self.namespace, self.dc_title)


class SkosLabel(models.Model):
    label = models.CharField(max_length=100, blank=True, help_text="The entities label or name.")
    label_type = models.CharField(
        max_length=30, blank=True, choices=LABEL_TYPES, help_text="The type of the label.")
    isoCode = models.CharField(
        max_length=3, blank=True, help_text="The ISO 639-3 code for the label's language.")

    def __str__(self):
        if self.label_type != "":
            return "{} @{} ({})".format(self.label, self.isoCode, self.label_type)
        else:
            return "{} @{}".format(self.label, self.isoCode)

    def get_absolute_url(self):
        return reverse('vocabs:skoslabel_detail', kwargs={'pk': self.id})


class SkosConcept(models.Model):
    pref_label = models.CharField(max_length=300, blank=True)
    pref_label_lang = models.CharField(max_length=3, blank=True, default="eng")
    scheme = models.ManyToManyField(SkosConceptScheme, blank=True)
    definition = models.TextField(blank=True)
    definition_lang = models.CharField(max_length=3, blank=True, default="eng")
    label = models.ManyToManyField(SkosLabel, blank=True)
    notation = models.CharField(max_length=300, blank=True)
    namespace = models.ForeignKey(SkosNamespace, blank=True, null=True)
    skos_broader = models.ManyToManyField('SkosConcept', blank=True, related_name="narrower")
    skos_narrower = models.ManyToManyField('SkosConcept', blank=True, related_name="broader")
    skos_related = models.ManyToManyField('SkosConcept', blank=True, related_name="related")
    skos_broadmatch = models.ManyToManyField('SkosConcept', blank=True, related_name="broadmatch")
    skos_exactmatch = models.ManyToManyField('SkosConcept', blank=True, related_name="exactmatch")
    skos_closematch = models.ManyToManyField('SkosConcept', blank=True, related_name="closematch")
    legacy_id = models.CharField(max_length=200, blank=True)

    @property
    def all_schemes(self):
        return ', '.join([x.dc_title for x in self.scheme.all()])

    def save(self, *args, **kwargs):
        if self.notation == "":
            temp_notation = slugify(self.pref_label, allow_unicode=True)
            concepts = len(SkosConcept.objects.filter(notation=temp_notation))
            if concepts < 1:
                self.notation = temp_notation
            else:
                self.notation = "{}-{}".format(temp_notation, concepts)
        else:
            pass

        if self.namespace is None:
            temp_namespace, _ = SkosNamespace.objects.get_or_create(
                namespace=DEFAULT_NAMESPACE, prefix=DEFAULT_PEFIX)
            temp_namespace.save()
            self.namespace = temp_namespace
        else:
            pass

        super(SkosConcept, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.pref_label)

    def get_absolute_url(self):
        return reverse('vocabs:skosconcept_detail', kwargs={'pk': self.id})
