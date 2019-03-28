from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

app_name = 'api'

urlpatterns = [
    path('auth/', include('api.urls_auth')),
    path('questionarios/', include('questionarios.api_urls')),
    path('docs/', include('api.urls_docs')),

    path('', include('questionarios.api_urls')),
]
