import requests
import re
import json
from django.shortcuts import (render, render_to_response, get_object_or_404, redirect)
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django_tables2 import RequestConfig
from .models import Place, AlternativeName, Institution, Person
from .forms import *
from .tables import PersonTable, InstitutionTable, PlaceTable
from .filters import PersonListFilter, InstitutionListFilter, PlaceListFilter
from webpage.utils import GenericListView, BaseCreateView, BaseUpdateView


class InstitutionListView(GenericListView):
    model = Institution
    table_class = InstitutionTable
    filter_class = InstitutionListFilter
    formhelper_class = InstitutionFilterFormHelper
    init_columns = [
        'id',
        'written_name',
    ]

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
            'page': 1, 'per_page': self.paginate_by
        }).configure(table)
        default_cols = self.init_columns
        all_cols = self.get_all_cols()
        selected_cols = self.request.GET.getlist("columns") + default_cols
        exclude_vals = [x for x in all_cols if x not in selected_cols]
        table.exclude = exclude_vals
        return table


class InstitutionDetailView(DetailView):
    model = Institution
    template_name = 'entities/institution_detail.html'


class InstitutionCreate(BaseCreateView):

    model = Institution
    form_class = InstitutionForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(InstitutionCreate, self).dispatch(*args, **kwargs)


class InstitutionUpdate(BaseUpdateView):

    model = Institution
    form_class = InstitutionForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(InstitutionUpdate, self).dispatch(*args, **kwargs)


class InstitutionDelete(DeleteView):
    model = Institution
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('entities:browse_institutions')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(InstitutionDelete, self).dispatch(*args, **kwargs)


class PersonListView(GenericListView):
    model = Person
    table_class = PersonTable
    filter_class = PersonListFilter
    formhelper_class = PersonFilterFormHelper
    init_columns = [
        'id',
        'name',
    ]

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
            'page': 1, 'per_page': self.paginate_by
        }).configure(table)
        default_cols = self.init_columns
        all_cols = self.get_all_cols()
        selected_cols = self.request.GET.getlist("columns") + default_cols
        exclude_vals = [x for x in all_cols if x not in selected_cols]
        table.exclude = exclude_vals
        return table


class PersonDetailView(DetailView):
    model = Person
    template_name = 'entities/person_detail.html'


class PersonCreate(BaseCreateView):

    model = Person
    form_class = PersonForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PersonCreate, self).dispatch(*args, **kwargs)


class PersonUpdate(BaseUpdateView):

    model = Person
    form_class = PersonForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PersonUpdate, self).dispatch(*args, **kwargs)


class PersonDelete(DeleteView):
    model = Person
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('entities:browse_entities')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PersonDelete, self).dispatch(*args, **kwargs)


class AlternativeNameListView(generic.ListView):
    context_object_name = 'object_list'

    def get_queryset(self):
        return AlternativeName.objects.all()


class AlternativeNameCreate(CreateView):

    model = AlternativeName
    form_class = AlternativeNameForm
    template_name = 'entities/alternativenames_create.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AlternativeNameCreate, self).dispatch(*args, **kwargs)


class AlternativeNameUpdate(UpdateView):

    model = AlternativeName
    form_class = AlternativeNameForm
    template_name = 'entities/alternativenames_create.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AlternativeNameUpdate, self).dispatch(*args, **kwargs)


class AlternativeNameDetailView(DetailView):
    model = AlternativeName
    template_name = 'entities/alternativenames_detail.html'


class AlternativeNameDelete(DeleteView):
    model = AlternativeName
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('browsing:browse_altnames')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AlternativeNameDelete, self).dispatch(*args, **kwargs)


class PlaceListView(GenericListView):
    model = Place
    table_class = PlaceTable
    filter_class = PlaceListFilter
    formhelper_class = PlaceFilterFormHelper
    init_columns = [
        'id',
        'name',
        'part_oc'
    ]

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
            'page': 1, 'per_page': self.paginate_by
        }).configure(table)
        default_cols = self.init_columns
        all_cols = self.get_all_cols()
        selected_cols = self.request.GET.getlist("columns") + default_cols
        exclude_vals = [x for x in all_cols if x not in selected_cols]
        table.exclude = exclude_vals
        return table


class PlaceDetailView(DetailView):
    model = Place
    template_name = 'entities/place_detail.html'


@login_required
def create_place(request):
    if request.method == "POST":
        form = PlaceFormCreate(request.POST)
        if form.is_valid():
            form.save()
            return redirect('browsing:browse_places')
        else:
            return render(request, 'entities/edit_places.html', {'form': form})
    else:
        form = PlaceFormCreate()
        return render(request, 'entities/edit_places.html', {'form': form})


@login_required
def edit_place(request, pk):
    instance = Place.objects.get(id=pk)
    username = "&username=digitalarchiv"
    if request.method == "GET":
        placeName = instance.name
        root = "http://api.geonames.org/searchJSON?q="
        params = "&fuzzy=0.6&lang=en&maxRows=100"
        url = root+placeName+params+username
        try:
            r = requests.get(url)
            response = r.text
            responseJSON = json.loads(response)
            responseJSON = responseJSON['geonames']
            form = PlaceForm(instance=instance)
            print(url)
            return render(
                request, 'entities/edit_places.html',
                {'object': instance, 'form': form, 'responseJSON': responseJSON}
            )
        except requests.exceptions.RequestException as e:
            url = e
        form = PlaceForm(instance=instance)

        responseJSON = "hansi"
        return render(
            request, 'entities/edit_places.html',
            {'object': instance, 'form': form, 'responseJSON': responseJSON}
        )
    else:
        form = PlaceForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
        return redirect('browsing:browse_places')


class PlaceDelete(DeleteView):
    model = Place
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('entities:browse_places')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PlaceDelete, self).dispatch(*args, **kwargs)
