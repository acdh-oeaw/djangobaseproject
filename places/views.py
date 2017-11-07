import requests
import re
import json
from django.shortcuts import (render, render_to_response, get_object_or_404, redirect)
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Place, AlternativeName
from .forms import PlaceForm, PlaceFormCreate, AlternativeNameForm


class AlternativeNameListView(generic.ListView):
    # template_name = "places/list_alternativenames.html"
    context_object_name = 'object_list'

    def get_queryset(self):
        return AlternativeName.objects.all()


class AlternativeNameCreate(CreateView):

    model = AlternativeName
    form_class = AlternativeNameForm
    template_name = 'places/alternativenames_create.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AlternativeNameCreate, self).dispatch(*args, **kwargs)


class AlternativeNameUpdate(UpdateView):

    model = AlternativeName
    form_class = AlternativeNameForm
    template_name = 'places/alternativenames_create.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AlternativeNameUpdate, self).dispatch(*args, **kwargs)


class AlternativeNameDetailView(DetailView):
    model = AlternativeName
    template_name = 'places/alternativenames_detail.html'


class PlaceDetailView(DetailView):
    model = Place
    template_name = 'places/place_detail.html'


class PlaceListView(generic.ListView):
    template_name = "places/list_places.html"
    context_object_name = 'object_list'

    def get_queryset(self):
        return Place.objects.all()


@login_required
def create_place(request):
    if request.method == "POST":
        form = PlaceFormCreate(request.POST)
        if form.is_valid():
            form.save()
            return redirect('places:place_list')
        else:
            return render(request, 'places/edit_places.html', {'form': form})
    else:
        form = PlaceFormCreate()
        return render(request, 'places/edit_places.html', {'form': form})


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
                request, 'places/edit_places.html',
                {'object': instance, 'form': form, 'responseJSON': responseJSON}
            )
        except requests.exceptions.RequestException as e:
            url = e
        form = PlaceForm(instance=instance)

        responseJSON = "hansi"
        return render(
            request, 'places/edit_places.html',
            {'object': instance, 'form': form, 'responseJSON': responseJSON}
        )
    else:
        form = PlaceForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
        return redirect('places:place_list')


class PlaceDelete(DeleteView):
    model = Place
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('places:place_list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PlaceDelete, self).dispatch(*args, **kwargs)
