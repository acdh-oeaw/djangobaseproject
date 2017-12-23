from django.shortcuts import render
from django.views.generic.edit import FormView
from pygermanet import load_germanet
from .forms import TokenForm

gn = load_germanet()


class TokenQuery(FormView):
    template_name = 'gnet/token_query.html'
    form_class = TokenForm
    success_url = '.'

    def form_valid(self, form, **kwargs):
        context = super(TokenQuery, self).get_context_data(**kwargs)
        cd = form.cleaned_data
        token = cd['token']
        context['token'] = None
        if token:
            lemma = gn.lemmatise("{}".format(token))
            if len(lemma) > 0:
                synsets = []
                for x in lemma:
                    for y in gn.synsets("{}".format(x)):
                        synsets.append(y)
            else:
                for y in gn.synsets("{}".format(lemma[0])):
                    synsets.append(y)
            synonyms = []
            for x in synsets:
                syn = {x.id: [
                    {'orthForm': [y.orthForm for y in x.lemmas]},
                    {'pos': [y.pos for y in x.lemmas]},
                    {'hypernyms': [y for y in x.hyponyms]}
                ]}
                synonyms.append(syn)
            context['token'] = token
            context['lemma'] = lemma
            context['synset_list'] = synonyms
        return render(self.request, self.template_name, context)
