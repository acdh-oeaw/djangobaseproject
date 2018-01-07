import spacy
from rest_framework.response import Response
from rest_framework.decorators import api_view
from pygermanet import load_germanet

gn = load_germanet()
nlp = spacy.load('de_core_news_sm')


@api_view()
def lemma(request):
    """
    get:
    Expects a `token` parameter (e.g. ?token=flog) which will be POS-tagged.

    """
    token = request.GET.get('token')
    enriched = {}
    if token:
        doc = nlp("{}".format(token))[0]
        enriched['token'] = token
        enriched['lemma'] = doc.lemma_
        enriched['pos'] = doc.pos_
        enriched['tag'] = doc.tag_
        return Response(enriched)
    else:
        return Response({'token': None})


@api_view()
def synset(request):
    """
    get:
    Expects a `token` parameter (e.g. ?token=flog) which will be checked against germanet.

    """
    token = request.GET.get('token')
    enriched = {}
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
            syn = {
                'orthForm': [y.orthForm for y in x.lemmas],
                'pos': [y.pos for y in x.lemmas],
                'hypernyms': ["{}".format(y) for y in x.hypernyms],
                'hypernym_paths': ["{}".format(y) for y in x.hypernym_paths]
            }
            synonyms.append(syn)
        enriched['token'] = token
        enriched['lemma'] = lemma
        enriched['synset_list'] = synonyms
        return Response(enriched)
    else:
        return Response({'token': None})
