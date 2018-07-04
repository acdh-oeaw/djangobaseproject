# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

app_name = 'bib'

urlpatterns = [
    url(r'^synczotero/$', views.sync_zotero, name="synczotero"),
    url(r'^synczotero/update$', views.update_zotitems, name="synczotero_update"),
]
