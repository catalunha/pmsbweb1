from django.urls import path, include
from rest_framework import routers

from relatorios.views_api import (
    RelatorioViewset,
    BlocoViewset,
    FiguraViewset,
)

relatorios_router = routers.DefaultRouter()

relatorios_router.register(r'relatorios', RelatorioViewset)
relatorios_router.register(r'blocos', BlocoViewset)
relatorios_router.register(r'figuras', FiguraViewset)

urlpatterns = [
    path('', include(relatorios_router.urls)),
]
