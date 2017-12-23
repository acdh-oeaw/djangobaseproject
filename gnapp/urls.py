from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers

router = routers.DefaultRouter()
urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
    url(r'^query/', include('gnet.urls', namespace='gnet')),
    url(r'^browsing/', include('browsing.urls', namespace='browsing')),
    url(r'^', include('webpage.urls', namespace='webpage')),
]
