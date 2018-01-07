from django.urls import include, path
from . import views, api_views

app_name = 'gnet'

urlpatterns = [
    path('token/', views.TokenQuery.as_view(), name='token'),
    path('textparser/', views.TextParser.as_view(), name='textparser'),
    path('lemmatize/', views.Lemmatize.as_view(), name='lemmatize'),
    path('lemma/', api_views.lemma, name='lemma'),
    path('synset/', api_views.synset, name='synset'),
    path('textparser-api/', api_views.textparser, name='textparser-api'),

]
