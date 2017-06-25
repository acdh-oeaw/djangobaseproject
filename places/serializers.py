from rest_framework import serializers
from .models import Place, AlternativeName


class AlternativeNameSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = AlternativeName
        fields = "__all__"


class PlaceHelperSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Place
        fields = "__all__"


class PlaceSerializer(serializers.HyperlinkedModelSerializer):
    alternative_name = AlternativeNameSerializer(many=True)
    part_of = PlaceHelperSerializer(many=False)

    class Meta:
        model = Place
        fields = "__all__"
