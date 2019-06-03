from django.conf.urls import url
from . import views
from . import special_views

app_name = 'infos'
urlpatterns = [
    url(
        r'^about-the-project/$',
        special_views.SpecialAboutView.as_view(),
        name='about-the-project'
    ),
    url(
        r'^about/$',
        views.AboutTheProjectListView.as_view(),
        name='about_browse'
    ),
    url(
        r'^about/detail/(?P<pk>[0-9]+)$',
        views.AboutTheProjectDetailView.as_view(),
        name='about_detail'
    ),
    url(
        r'^about/create/$',
        views.AboutTheProjectCreate.as_view(),
        name='about_create'
    ),
    url(
        r'^about/edit/(?P<pk>[0-9]+)$',
        views.AboutTheProjectUpdate.as_view(),
        name='about_edit'
    ),
    url(
        r'^about/delete/(?P<pk>[0-9]+)$',
        views.AboutTheProjectDelete.as_view(),
        name='about_delete'),
]
