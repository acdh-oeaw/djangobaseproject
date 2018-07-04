import requests
from django.conf import settings
from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from . models import ZotItem
from . zot_utils import items_to_dict, create_zotitem

from .models import Book, Reference
from .forms import ReferenceForm


library_id = settings.Z_ID
library_type = settings.Z_LIBRARY_TYPE
api_key = settings.Z_API_KEY


class BaseCreateView(CreateView):
    model = None
    form_class = None
    template_name = 'bib/generic_create.html'

    def get_context_data(self, **kwargs):
        context = super(BaseCreateView, self).get_context_data()
        context['docstring'] = "{}".format(self.model.__doc__)
        if self.model.__name__.endswith('s'):
            context['class_name'] = "{}".format(self.model.__name__)
        else:
            context['class_name'] = "{}s".format(self.model.__name__)
        return context


class BaseUpdateView(UpdateView):
    model = None
    form_class = None
    template_name = 'archiv/generic_create.html'

    def get_context_data(self, **kwargs):
        context = super(BaseUpdateView, self).get_context_data()
        context['docstring'] = "{}".format(self.model.__doc__)
        if self.model.__name__.endswith('s'):
            context['class_name'] = "{}".format(self.model.__name__)
        else:
            context['class_name'] = "{}s".format(self.model.__name__)
        return context


class ReferenceDetailView(DetailView):
    model = Reference
    template_name = 'bib/reference_detail.html'


class ReferenceCreate(BaseCreateView):

    model = Reference
    form_class = ReferenceForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ReferenceCreate, self).dispatch(*args, **kwargs)


class ReferenceUpdate(BaseUpdateView):

    model = Reference
    form_class = ReferenceForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ReferenceUpdate, self).dispatch(*args, **kwargs)


class ReferenceDelete(DeleteView):
    model = Reference
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('browsing:browse_references')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ReferenceDelete, self).dispatch(*args, **kwargs)


def sync_zotero(request):
    """ renders a simple template with a button to trigger sync_zotero_action function """
    context = {}
    return render(request, 'bib/synczotero.html', context)


@login_required
def update_zotitems(request):
    """ fetches all items with higher version number then the highest stored in db """
    context = {}
    context["saved"] = []
    limit = None
    since = None
    context["books_before"] = ZotItem.objects.all().count()
    first_object = ZotItem.objects.all()[:1].get()
    since = first_object.zot_version
    items = items_to_dict(library_id, library_type, api_key, limit=limit, since_version=since)
    for x in items['bibs']:
        temp_item = create_zotitem(x)
        saved.append(temp_item)
    context["books_after"] = ZotItem.objects.all().count()
    return render(request, 'bib/synczotero_action.html', context)
