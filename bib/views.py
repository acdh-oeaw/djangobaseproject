import requests
from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import Book, Reference
from .forms import ReferenceForm
from django.conf import settings


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
    try:
        context['base_url'] = settings.Z_COLLECTION_URL
        context['collection_title'] = settings.Z_TITLE
    except:
        context['base_url'] = ''
        context['collection_title'] = 'PLEASE PROVIDE TITEL IN SETTINGS FILE'
    return render(request, 'bib/synczotero.html', context)


@login_required
def sync_zotero_action(request):
    """ fetches the last n items form zoter and syncs it with the bib entries in defc-db"""
    root = "https://api.zotero.org/"
    if settings.Z_COLLECTION:
        try:
            params = "{}/{}/collections/{}/items/top?v=3&key={}".format(
                settings.Z_ID_TYPE, settings.Z_ID, settings.Z_COLLECTION, settings.Z_API_KEY
            )
        except AttributeError as err:
            context = {}
            context['error'] = "{}".format(err)
            return render(request, 'bib/synczotero_action.html', context)
    else:
        try:
            params = "{}/{}/items/top?v=3&key={}".format(
                settings.Z_ID_TYPE, settings.Z_ID, settings.Z_API_KEY
            )
        except AttributeError as err:
            context = {}
            context['error'] = "{}".format(err)
            return render(request, 'bib/synczotero_action.html', context)
    try:
        limit = settings.Z_LIMIT
    except AttributeError:
        limit = "25"
    url = root + params + "&sort=dateModified&limit={}".format(limit)
    print(url)
    books_before = len(Book.objects.all())
    try:
        r = requests.get(url)
        error = "No errors from ZoteroAPI"
    except:
        error = "aa! errors! The API didn´t response with a proper json-file"
    try:
        response = r.json()
    except:
        response = None

    if response:
        failed = []
        saved = []
        for x in response:
            try:
                x["data"]["creators"][0]
                try:
                    x["data"]["creators"][0]["name"]
                    name = x["data"]["creators"][0]["name"]
                except:
                    firstname = x["data"]["creators"][0]["firstName"]
                    lastname = x["data"]["creators"][0]["lastName"]
                    name = "{}, {}".format(lastname, firstname)
            except:
                name = "no name provided"
            NewBook = Book(
                zoterokey=x["data"]["key"], item_type=x["data"]["itemType"],
                author=name,
                title=x["data"]["title"],
                short_title=x["data"]["shortTitle"]
            )
            try:
                NewBook.save()
                saved.append(NewBook)
            except:
                failed(x['data'])
        books_after = len(Book.objects.all())
        context = {}
        context["error"] = error
        context["saved"] = saved
        context["failed"] = failed
        context["books_before"] = [books_before]
        context["books_after"] = [books_after]
        return render(request, 'bib/synczotero_action.html', context)
    else:
        context = {}
        context["error"] = "something went wrong, please check your zotero settings"
        return render(request, 'bib/synczotero_action.html', context)
