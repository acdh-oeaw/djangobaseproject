# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

app_name = 'bib'

urlpatterns = [
    url(r'^synczotero/$', views.sync_zotero, name="synczotero"),
    url(r'^synczotero/result$', views.sync_zotero_action, name="synczotero_action"),
    url(r'^reference/detail/(?P<pk>[0-9]+)$', views.ReferenceDetailView.as_view(),
        name='reference_detail'),
    url(r'^reference/create/$', views.ReferenceCreate.as_view(),
        name='reference_create'),
    url(r'^reference/edit/(?P<pk>[0-9]+)$', views.ReferenceUpdate.as_view(),
        name='reference_edit'),
    url(r'^reference/delete/(?P<pk>[0-9]+)$', views.ReferenceDelete.as_view(),
        name='reference_delete'),
]
