# generated by appcreator
import django_tables2 as tables
from django_tables2.utils import A
from . models import AboutTheProject


class AboutTheProjectTable(tables.Table):

    id = tables.LinkColumn(verbose_name='ID')

    class Meta:
        model = AboutTheProject
        sequence = ('id',)
        attrs = {"class": "table table-responsive table-hover"}
