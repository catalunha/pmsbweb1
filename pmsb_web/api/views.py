from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.models import MobileApp

class VersaoAPIView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request, formt=None):
        """
        Retorna versão atual do app mobile
        """
        latest = MobileApp.latest()

        return Response(latest)