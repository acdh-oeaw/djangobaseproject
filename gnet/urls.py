from django.urls import include, path
from . import views

app_name = 'gnet'

urlpatterns = [
    path('token/', views.TokenQuery.as_view(), name='token-query'),
]
