from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from api.views import VersaoAPIView, VersaoAppAPIView

app_name = 'api'

urlpatterns = [
    path('versao/', VersaoAPIView.as_view(), name='versao'),
    path('versao/app/', VersaoAppAPIView.as_view(), name='versao_app'),
    path('auth/', include('api.urls_auth')),
    path('questionarios/', include('questionarios.api_urls')),
    path('docs/', include('api.urls_docs')),
    path('contas/', include('conta.urls_api')),
    path('relatorios/', include('relatorios.urls_api')),

]
