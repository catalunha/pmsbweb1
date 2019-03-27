from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

app_name = 'api'

urlpatterns = [
    path('auth/', include('api.urls_auth')),
    path('questionarios/', include('questionarios.api_urls')),
    path('', include('questionarios.api_urls')),
]

if settings.DEBUG:    
    urlpatterns += [
        path('docs/swagger', get_swagger_view(title="PMSB API")),
    ]
