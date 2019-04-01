from django.urls import path, include
from rest_framework import routers

from .views_api import (
    UserViewSet,
    CargoViewSet,
    DepartamentoViewSet,
)

contas_router = routers.DefaultRouter()

contas_router.register(r'users', UserViewSet)
contas_router.register(r'cargos', CargoViewSet)
contas_router.register(r'departamentos', DepartamentoViewSet)

urlpatterns = [
    path('', include(contas_router.urls)),
]
