from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated

from .models import User, Cargo, Departamento
from .serializers import UserSerializer, CargoSerializer, DepartamentoSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (DjangoModelPermissions,)


class CargoViewSet(viewsets.ModelViewSet):
    serializer_class = CargoSerializer
    queryset = Cargo.objects.all()
    permission_classes = (DjangoModelPermissions,)


class DepartamentoViewSet(viewsets.ModelViewSet):
    serializer_class = DepartamentoSerializer
    queryset = Departamento.objects.all()
    permission_classes = (DjangoModelPermissions,)
