import time
import datetime
from django.http import HttpResponse
import rdflib
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef, RDFS, ConjunctiveGraph
from rdflib.namespace import DC, FOAF, RDFS
from rdflib.namespace import SKOS
from django_tables2 import SingleTableView, RequestConfig
from .filters import *
from .forms import *
from .tables import *
from entities.models import Place, Institution
from entities.serializer_arche import *


class GenericListView(SingleTableView):
    filter_class = None
    formhelper_class = None
    context_filter_name = 'filter'
    paginate_by = 25
    template_name = 'browsing/generic_list.html'

    def get_queryset(self, **kwargs):
        qs = super(GenericListView, self).get_queryset()
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        self.filter.form.helper = self.formhelper_class()
        return self.filter.qs

    def get_table(self, **kwargs):
        table = super(GenericListView, self).get_table()
        RequestConfig(self.request, paginate={
            'page': 1, 'per_page': self.paginate_by}).configure(table)
        return table

    def get_context_data(self, **kwargs):
        context = super(GenericListView, self).get_context_data()
        context[self.context_filter_name] = self.filter
        context['docstring'] = "{}".format(self.model.__doc__)
        if self.model.__name__.endswith('s'):
            context['class_name'] = "{}".format(self.model.__name__)
        else:
            context['class_name'] = "{}s".format(self.model.__name__)
        try:
            context['get_arche_dump'] = self.model.get_arche_dump()
        except AttributeError:
            context['get_arche_dump'] = None
        try:
            context['create_view_link'] = self.model.get_createview_url()
        except AttributeError:
            context['create_view_link'] = None
        return context


class AlternativeNameListView(GenericListView):
    model = AlternativeName
    table_class = AlternativeNameTable
    filter_class = AlternativeNameListFilter
    formhelper_class = AlternativeNameFilterFormHelper
    init_columns = ['id', 'name', 'part_of']

    def get_all_cols(self):
        all_cols = list(self.table_class.base_columns.keys())
        return all_cols

    def get_context_data(self, **kwargs):
        context = super(AlternativeNameListView, self).get_context_data()
        context[self.context_filter_name] = self.filter
        togglable_colums = [x for x in self.get_all_cols() if x not in self.init_columns]
        context['togglable_colums'] = togglable_colums
        return context

    def get_table(self, **kwargs):
        table = super(GenericListView, self).get_table()
        RequestConfig(self.request, paginate={'page': 1, 'per_page': self.paginate_by}).configure(table)
        default_cols = self.init_columns
        all_cols = self.get_all_cols()
        selected_cols = self.request.GET.getlist("columns") + default_cols
        exclude_vals = [x for x in all_cols if x not in selected_cols]
        table.exclude = exclude_vals
        return table


class PersonRDFView(GenericListView):
    model = Person
    table_class = PersonTable
    template_name = 'browsing/rdflib_template.txt'
    filter_class = PersonListFilter
    formhelper_class = GenericFilterFormHelper

    def render_to_response(self, context):
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')
        response = HttpResponse(content_type='application/xml; charset=utf-8')
        filename = "places_{}".format(timestamp)
        response['Content-Disposition'] = 'attachment; filename="{}.rdf"'.format(filename)
        g = person_to_arche(self.get_queryset())
        get_format = self.request.GET.get('format', default='n3')
        result = g.serialize(destination=response, format=get_format)
        return response


class PlaceRDFView(GenericListView):
    model = Place
    table_class = PlaceTable
    template_name = 'browsing/rdflib_template.txt'
    filter_class = PlaceListFilter
    formhelper_class = GenericFilterFormHelper

    def render_to_response(self, context):
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')
        response = HttpResponse(content_type='application/xml; charset=utf-8')
        filename = "places_{}".format(timestamp)
        response['Content-Disposition'] = 'attachment; filename="{}.rdf"'.format(filename)
        g = place_to_arche(self.get_queryset())
        get_format = self.request.GET.get('format', default='n3')
        result = g.serialize(destination=response, format=get_format)
        return response


class InstitutionRDFView(GenericListView):
    model = Institution
    table_class = InstitutionTable
    template_name = 'browsing/rdflib_template.txt'
    filter_class = InstitutionListFilter
    formhelper_class = GenericFilterFormHelper

    def render_to_response(self, context):
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')
        response = HttpResponse(content_type='application/xml; charset=utf-8')
        filename = "institutions_{}".format(timestamp)
        response['Content-Disposition'] = 'attachment; filename="{}.rdf"'.format(filename)
        g = inst_to_arche(self.get_queryset())
        get_format = self.request.GET.get('format', default='n3')
        result = g.serialize(destination=response, format=get_format)
        return response


class InstitutionListView(GenericListView):
    model = Institution
    table_class = InstitutionTable
    filter_class = InstitutionListFilter
    formhelper_class = InstitutionFilterFormHelper
    init_columns = ['id', 'written_name']

    def get_all_cols(self):
        all_cols = list(self.table_class.base_columns.keys())
        return all_cols

    def get_context_data(self, **kwargs):
        context = super(InstitutionListView, self).get_context_data()
        context[self.context_filter_name] = self.filter
        togglable_colums = [x for x in self.get_all_cols() if x not in self.init_columns]
        context['togglable_colums'] = togglable_colums
        return context

    def get_table(self, **kwargs):
        table = super(GenericListView, self).get_table()
        RequestConfig(self.request, paginate={
            'page': 1, 'per_page': self.paginate_by}).configure(table)
        default_cols = self.init_columns
        all_cols = self.get_all_cols()
        selected_cols = self.request.GET.getlist("columns") + default_cols
        exclude_vals = [x for x in all_cols if x not in selected_cols]
        table.exclude = exclude_vals
        return table


class PlaceListView(GenericListView):
    model = Place
    table_class = PlaceTable
    filter_class = PlaceListFilter
    formhelper_class = PlaceFilterFormHelper
    init_columns = ['id', 'name', 'lat', 'lng']

    def get_all_cols(self):
        all_cols = list(self.table_class.base_columns.keys())
        return all_cols

    def get_context_data(self, **kwargs):
        context = super(PlaceListView, self).get_context_data()
        context[self.context_filter_name] = self.filter
        togglable_colums = [x for x in self.get_all_cols() if x not in self.init_columns]
        context['togglable_colums'] = togglable_colums
        return context

    def get_table(self, **kwargs):
        table = super(GenericListView, self).get_table()
        RequestConfig(self.request, paginate={
            'page': 1, 'per_page': self.paginate_by}).configure(table)
        default_cols = self.init_columns
        all_cols = self.get_all_cols()
        selected_cols = self.request.GET.getlist("columns") + default_cols
        exclude_vals = [x for x in all_cols if x not in selected_cols]
        table.exclude = exclude_vals
        return table


class PersonListView(GenericListView):
    model = Person
    table_class = PersonTable
    filter_class = PersonListFilter
    formhelper_class = PersonFilterFormHelper
    init_columns = ['id', 'written_name', 'name', 'forename']

    def get_all_cols(self):
        all_cols = list(self.table_class.base_columns.keys())
        return all_cols

    def get_context_data(self, **kwargs):
        context = super(PersonListView, self).get_context_data()
        context[self.context_filter_name] = self.filter
        togglable_colums = [x for x in self.get_all_cols() if x not in self.init_columns]
        context['togglable_colums'] = togglable_colums
        return context

    def get_table(self, **kwargs):
        table = super(GenericListView, self).get_table()
        RequestConfig(self.request, paginate={
            'page': 1, 'per_page': self.paginate_by}).configure(table)
        default_cols = self.init_columns
        all_cols = self.get_all_cols()
        selected_cols = self.request.GET.getlist("columns") + default_cols
        exclude_vals = [x for x in all_cols if x not in selected_cols]
        table.exclude = exclude_vals
        return table
