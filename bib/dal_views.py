from dal import autocomplete
from django.db.models import Q
from .models import *


class BookAC(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Book.objects.all()

        if self.q:
            qs = qs.filter(
                Q(title__icontains=self.q) | Q(author__icontains=self.q)
            )

        return qs


class ReferenceAC(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Reference.objects.all()

        if self.q:
            qs = qs.filter(
                Q(zotero_item__title__icontains=self.q) | Q(zotero_item__author__icontains=self.q)
            )

        return qs
