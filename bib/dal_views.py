from dal import autocomplete
from django.db.models import Q
from . models import ZotItem


class ZotItemAC(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = ZotItem.objects.all()

        if self.q:
            qs = qs.filter(
                Q(zot_title__icontains=self.q) |
                Q(zot_creator__icontains=self.q) |
                Q(zot_pub_title__icontains=self.q) |
                Q(zot_date__icontains=self.q)
            )

        return qs
