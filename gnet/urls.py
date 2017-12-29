from django.urls import include, path
from . import views, api_views

app_name = 'gnet'

urlpatterns = [
    path('token/', views.TokenQuery.as_view(), name='token'),
    path('lemmatize/', views.Lemmatize.as_view(), name='lemmatize'),
    path('lemma/', api_views.lemma, name='lemma'),

]
