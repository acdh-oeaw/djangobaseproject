import os
from SPARQLWrapper import SPARQLWrapper, JSON
from django.http import Http404
from django.conf import settings
from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import QueryForm
from .models import Query, endpoint


class QueryView(FormView):
    template_name = 'sparql/query_view.html'
    form_class = QueryForm
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super(QueryView, self).get_context_data(**kwargs)
        context['examples'] = Query.objects.all()
        return context

    def form_valid(self, form, **kwargs):
        context = self.get_context_data()
        cd = form.cleaned_data
        query = cd['query']
        context['query'] = query
        sparql = SPARQLWrapper(endpoint)
        print(endpoint)
        try:
            sparql.setQuery(query)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            context['results'] = results['results']
            return render(self.request, self.template_name, context)
        except:
            raise Http404("Bad Query, try another")
