from rest_framework import serializers
from .models import SkosConcept, SkosConceptScheme, SkosLabel, SkosNamespace


class SkosLabelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SkosLabel
        fields = ('label', 'label_type', 'isoCode')


class SkosNamespaceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SkosNamespace
        fields = ('namespace', 'prefix')


class SkosConceptSchemeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SkosConceptScheme
        fields = ('dc_title', 'namespace', 'dct_creator', 'legacy_id')


class SkosConceptSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = SkosConcept
        fields = (
            'id', 'url', 'scheme',
            'pref_label', 'pref_label_lang',
            'definition', 'definition_lang',
            'other_label',
            'notation',
            'broader_concept',
            'skos_broader', 'broader', 'skos_narrower', 'narrower',
            'skos_related', 'related',
            'skos_broadmatch', 'narrowmatch',
            'skos_exactmatch', 'exactmatch', 'skos_closematch', 'closematch',

            'legacy_id'
        )
