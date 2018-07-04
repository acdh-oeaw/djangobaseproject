from rest_framework import viewsets
from .serializers import ZotItemSerializer
from .models import ZotItem


class ZotItemViewSet(viewsets.ModelViewSet):
    queryset = ZotItem.objects.all()
    serializer_class = ZotItemSerializer
