from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings
from django.views.generic import TemplateView
from api.models import MobileApp

class VersaoAPIView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request, formt=None):
        """
        Retorna versão atual da api
        """
        
        return Response(settings.API_VERSION)

class VersaoAppAPIView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request, formt=None):
        """
        Retorna versão atual do app mobile
        """
        latest = MobileApp.latest()
        
        if latest is None:
            latest_text = "0.0.0"
        else:
            latest_text = latest.versao()
        
        return Response(latest_text)

class IndexTemplateView(TemplateView):
    template_name = "api/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mobileapp'] = MobileApp.latest() or True
        return context
