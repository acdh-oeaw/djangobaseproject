from rest_framework import serializers
from .models import ZotItem


class ZotItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ZotItem
        fields = "__all__"
