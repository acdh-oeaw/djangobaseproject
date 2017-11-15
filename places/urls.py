from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^altnames/$', views.AlternativeNameListView.as_view(), name='alternativename_list'),
    url(r'^altnames/detail/(?P<pk>[0-9]+)$', views.AlternativeNameDetailView.as_view(),
        name='alternativename_detail'),
    url(r'^altnames/create/$', views.AlternativeNameCreate.as_view(),
        name='alternativename_create'),
    url(r'^altnames/edit/(?P<pk>[0-9]+)$', views.AlternativeNameUpdate.as_view(),
        name='alternativename_edit'),
    url(r'^$', views.PlaceListView.as_view(), name='place_list'),
    url(r'^create/$', views.create_place, name='place_create'),
    url(r'^detail/(?P<pk>[0-9]+)$', views.PlaceDetailView.as_view(), name='place_detail'),
    url(r'^edit/(?P<pk>[0-9]+)$', views.edit_place, name='place_edit'),
    url(r'^delete/(?P<pk>[0-9]+)$', views.PlaceDelete.as_view(), name='place_delete'),
    url(r'^institutions/detail/(?P<pk>[0-9]+)$', views.InstitutionDetailView.as_view(),
        name='institution_detail'),
    url(r'^institutions/edit/(?P<pk>[0-9]+)$', views.InstitutionUpdate.as_view(),
        name='institution_edit'),
    url(r'^institutions/create/$', views.InstitutionCreate.as_view(),
        name='institution_create'),
    url(r'^persons/detail/(?P<pk>[0-9]+)$', views.PersonDetailView.as_view(),
        name='person_detail'),
]
