from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'places/$', views.PlaceListView.as_view(), name='browse_places'),
    url(r'places-rdf/$', views.PlaceRDFView.as_view(), name='rdf_places'),
    url(r'persons/$', views.PersonListView.as_view(), name='browse_persons'),
    url(r'persons-rdf/$', views.PersonRDFView.as_view(), name='rdf_persons'),
    url(r'institutions/$', views.InstitutionListView.as_view(), name='browse_institutions'),
    url(r'institutions-rdf/$', views.InstitutionRDFView.as_view(), name='rdf_institutions'),
]
