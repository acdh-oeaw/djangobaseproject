import django_tables2 as tables
from django_tables2.utils import A
from places.models import *


class PlaceTable(tables.Table):
    name = tables.LinkColumn(
        'places:place_detail',
        args=[A('pk')], verbose_name='Name'
    )
    part_of = tables.Column()

    class Meta:
        model = Place
        sequence = ('id', 'name',)
        attrs = {"class": "table table-responsive table-hover"}
