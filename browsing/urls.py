from django.conf.urls import url
from . import views

app_name = 'browsing'

urlpatterns = [
    url(r'^merge-objects/$', views.merge_objects, name='merge_objects'),
]
