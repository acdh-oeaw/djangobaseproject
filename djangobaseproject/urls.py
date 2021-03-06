from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from rest_framework import routers
from vocabs import api_views

router = routers.DefaultRouter()
router.register(r'skosconceptschemes', api_views.SkosConceptSchemeViewSet)
router.register(r'skoscollections', api_views.SkosCollectionViewSet)
router.register(r'skosconcepts', api_views.SkosConceptViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
    url(r'^browsing/', include('browsing.urls', namespace='browsing')),
    url(r'^info/', include('infos.urls', namespace='info')),
    url(r'^vocabs/', include('vocabs.urls', namespace='vocabs')),
    url(r'^vocabs-ac/', include('vocabs.dal_urls', namespace='vocabs-ac')),
    url(
        r'^gn-places-ac/',
        include('gn_places.dal_urls', namespace='gn_places-ac')
    ),
    url(r'^', include('webpage.urls', namespace='webpage')),
]


handler404 = 'webpage.views.handler404'
