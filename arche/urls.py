from django.conf.urls import url
from . import views

app_name = 'arche'

urlpatterns = [
    url(r'^projects/$', views.ProjectListView.as_view(), name='browse_projects'),
    url(r'^project/detail/(?P<pk>[0-9]+)$', views.ProjectDetailView.as_view(),
        name='project_detail'),
    url(r'^project/create/$', views.ProjectCreate.as_view(),
        name='project_create'),
    url(r'^project/edit/(?P<pk>[0-9]+)$', views.ProjectUpdate.as_view(),
        name='project_edit'),
    url(r'^project/delete/(?P<pk>[0-9]+)$', views.ProjectDelete.as_view(),
        name='project_delete'),
    url(r'projects-rdf/$', views.ProjectRDFView.as_view(), name='rdf_projects'),
    url(r'^collections/$', views.CollectionListView.as_view(), name='browse_collections'),
    url(r'^collection/detail/(?P<pk>[0-9]+)$', views.CollectionDetailView.as_view(),
        name='collection_detail'),
    url(r'^collection/create/$', views.CollectionCreate.as_view(),
        name='collection_create'),
    url(r'^collection/edit/(?P<pk>[0-9]+)$', views.CollectionUpdate.as_view(),
        name='collection_edit'),
    url(r'^collection/delete/(?P<pk>[0-9]+)$', views.CollectionDelete.as_view(),
        name='collection_delete'),
    url(r'collections-rdf/$', views.CollectionRDFView.as_view(), name='rdf_collections'),
]
