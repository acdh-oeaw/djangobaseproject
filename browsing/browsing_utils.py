import datetime
import time
import pandas as pd
import django_filters
from django.conf import settings
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Div, MultiField, HTML
from django_tables2 import SingleTableView, RequestConfig
from . models import BrowsConf

if 'bib' in settings.INSTALLED_APPS:
    from charts.models import ChartConfig
    from charts.views import create_payload


class GenericFilterFormHelper(FormHelper):

    def __init__(self, *args, **kwargs):
        super(GenericFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))


django_filters.filters.LOOKUP_TYPES = [
    ('', '---------'),
    ('exact', 'Is equal to'),
    ('iexact', 'Is equal to (case insensitive)'),
    ('not_exact', 'Is not equal to'),
    ('lt', 'Lesser than/before'),
    ('gt', 'Greater than/after'),
    ('gte', 'Greater than or equal to'),
    ('lte', 'Lesser than or equal to'),
    ('startswith', 'Starts with'),
    ('endswith', 'Ends with'),
    ('contains', 'Contains'),
    ('icontains', 'Contains (case insensitive)'),
    ('not_contains', 'Does not contain'),
]


class GenericListView(SingleTableView):
    filter_class = None
    formhelper_class = None
    context_filter_name = 'filter'
    paginate_by = 25
    template_name = 'browsing/generic_list.html'
    init_columns = []

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
        default_cols = self.init_columns
        all_cols = self.get_all_cols()
        selected_cols = self.request.GET.getlist("columns") + default_cols
        exclude_vals = [x for x in all_cols if x not in selected_cols]
        table.exclude = exclude_vals
        return table

    def get_context_data(self, **kwargs):
        context = super(GenericListView, self).get_context_data()
        togglable_colums = [x for x in self.get_all_cols() if x not in self.init_columns]
        context['togglable_colums'] = togglable_colums
        context[self.context_filter_name] = self.filter
        context['docstring'] = "{}".format(self.model.__doc__)
        if self.model._meta.verbose_name_plural:
            context['class_name'] = "{}".format(self.model._meta.verbose_name.title())
        else:
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
        try:
            context['download'] = self.model.get_dl_url()
        except AttributeError:
            context['download'] = None
        model_name = self.model.__name__.lower()
        context['entity'] = model_name
        context['conf_items'] = list(
            BrowsConf.objects.filter(model_name=model_name)
            .values_list('field_path', 'label')
        )
        print(context['conf_items'])
        if 'bib' in settings.INSTALLED_APPS:
            context['vis_list'] = ChartConfig.objects.filter(model_name=model_name)
            context['property_name'] = self.request.GET.get('property')
            context['charttype'] = self.request.GET.get('charttype')
            if context['charttype'] and context['property_name']:
                qs = self.get_queryset()
                chartdata = create_payload(
                    context['entity'],
                    context['property_name'],
                    context['charttype'],
                    qs
                )
                context = dict(context, **chartdata)
        return context

    def render_to_response(self, context, **kwargs):
        download = self.request.GET.get('sep', None)
        if download:
            sep = self.request.GET.get('sep', ',')
            timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')
            filename = "export_{}".format(timestamp)
            response = HttpResponse(content_type='text/csv')
            if context['conf_items']:
                conf_items = context['conf_items']
                try:
                    df = pd.DataFrame(
                        list(
                            self.model.objects.all().values_list(*[x[0] for x in conf_items])
                        ),
                        columns=[x[1] for x in conf_items]
                    )
                except AssertionError:
                    response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(filename)
                    return response
            else:
                response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(filename)
                return response
            if sep == "comma":
                df.to_csv(response, sep=',', index=False)
            elif sep == "semicolon":
                df.to_csv(response, sep=';', index=False)
            elif sep == "tab":
                df.to_csv(response, sep='\t', index=False)
            else:
                df.to_csv(response, sep=',', index=False)
            response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(filename)
            return response
        else:
            response = super(GenericListView, self).render_to_response(context)
            return response


class BaseCreateView(CreateView):
    model = None
    form_class = None
    template_name = 'browsing/generic_create.html'

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
    template_name = 'browsing/generic_create.html'

    def get_context_data(self, **kwargs):
        context = super(BaseUpdateView, self).get_context_data()
        context['docstring'] = "{}".format(self.model.__doc__)
        if self.model.__name__.endswith('s'):
            context['class_name'] = "{}".format(self.model.__name__)
        else:
            context['class_name'] = "{}s".format(self.model.__name__)
        return context
