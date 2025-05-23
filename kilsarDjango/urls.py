from django.contrib.auth.models import User
from django.urls import include, path
from rest_framework import routers, serializers, viewsets

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api/todo/', include('todolist.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]