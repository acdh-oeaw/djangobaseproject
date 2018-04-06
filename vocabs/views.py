from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django_tables2 import SingleTableView, RequestConfig
from .models import SkosConcept, SkosConceptScheme, SkosLabel
from .forms import *
from .tables import SkosConceptTable
from .filters import SkosConceptListFilter


class GenericListView(SingleTableView):
    filter_class = None
    formhelper_class = None
    context_filter_name = 'filter'
    paginate_by = 25
    template_name = 'vocabs/generic_list.html'

    def get_all_cols(self):
        all_cols = list(self.table_class.base_columns.keys())
        return all_cols

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


class SkosConceptListView(GenericListView):
    model = SkosConcept
    table_class = SkosConceptTable
    filter_class = SkosConceptListFilter
    formhelper_class = SkosConceptFormHelper
    init_columns = ['id', 'broader_concept', 'pref_label', 'all_schemes']

    def get_all_cols(self):
        all_cols = list(self.table_class.base_columns.keys())
        return all_cols

    def get_context_data(self, **kwargs):
        context = super(SkosConceptListView, self).get_context_data()
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


class SkosConceptDetailView(DetailView):

    model = SkosConcept
    template_name = 'vocabs/skosconcept_detail.html'


class SkosConceptCreate(CreateView):

    model = SkosConcept
    template_name = 'vocabs/skosconcept_create.html'
    form_class = SkosConceptForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SkosConceptCreate, self).dispatch(*args, **kwargs)


class SkosConceptUpdate(UpdateView):

    model = SkosConcept
    form_class = SkosConceptForm
    template_name = 'vocabs/skosconcept_create.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SkosConceptUpdate, self).dispatch(*args, **kwargs)


class SkosConceptDelete(DeleteView):
    model = SkosConcept
    template_name = 'vocabs/confirm_delete.html'
    success_url = reverse_lazy('vocabs:browse_vocabs')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SkosConceptDelete, self).dispatch(*args, **kwargs)


#####################################################
#   ConceptScheme
#####################################################


class SkosConceptSchemeDetailView(DetailView):

    model = SkosConceptScheme
    template_name = 'vocabs/skosconceptscheme_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SkosConceptSchemeDetailView, self).get_context_data(**kwargs)
        context["concepts"] = SkosConcept.objects.filter(scheme=self.kwargs.get('pk'))
        return context


class SkosConceptSchemeListView(ListView):

    model = SkosConceptScheme
    template_name = 'vocabs/skosconceptscheme_list.html'


class SkosConceptSchemeCreate(CreateView):

    model = SkosConceptScheme
    form_class = SkosConceptSchemeForm
    template_name = 'vocabs/skosconceptscheme_create.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SkosConceptSchemeCreate, self).dispatch(*args, **kwargs)


class SkosConceptSchemeUpdate(UpdateView):

    model = SkosConceptScheme
    form_class = SkosConceptSchemeForm
    template_name = 'vocabs/skosconceptscheme_create.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SkosConceptSchemeUpdate, self).dispatch(*args, **kwargs)


###################################################
# SkosLabel
###################################################


class SkosLabelDetailView(DetailView):

    model = SkosLabel
    template_name = 'vocabs/skoslabel_detail.html'


class SkosLabelListView(ListView):

    model = SkosLabel
    template_name = 'vocabs/skoslabel_list.html'


class SkosLabelCreate(CreateView):

    model = SkosLabel
    template_name = 'vocabs/skoslabel_create.html'
    form_class = SkosLabelForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SkosLabelCreate, self).dispatch(*args, **kwargs)


class SkosLabelUpdate(UpdateView):

    model = SkosLabel
    form_class = SkosLabelForm
    template_name = 'vocabs/skoslabel_create.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SkosLabelUpdate, self).dispatch(*args, **kwargs)
