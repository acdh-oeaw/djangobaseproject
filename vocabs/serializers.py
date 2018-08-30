from rest_framework import serializers
from .models import SkosConcept, SkosConceptScheme, SkosLabel, SkosNamespace, Metadata


class MetadataSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Metadata
        fields = '__all__'


class SkosLabelSerializer(serializers.HyperlinkedModelSerializer):
    #url = serializers.HyperlinkedIdentityField(view_name='skoslabel-detail')
    class Meta:
        model = SkosLabel
        fields = ('url', 'label', 'label_type', 'isoCode')


class SkosNamespaceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SkosNamespace
        fields = ('namespace', 'prefix')


class SkosConceptSchemeSerializer(serializers.HyperlinkedModelSerializer):
    has_concepts = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='skosconcept-detail')

    class Meta:
        model = SkosConceptScheme
        fields = ('dc_title', 'namespace', 'dct_creator', 'legacy_id', 'has_concepts')


class SkosConceptSerializer(serializers.HyperlinkedModelSerializer):
    scheme = SkosConceptSchemeSerializer(many=True, read_only=True)
    other_label = SkosLabelSerializer(many=True, read_only=True)

    class Meta:
        model = SkosConcept
        fields = (
            'id', 'url',
            'pref_label', 'pref_label_lang',
            'scheme',
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
