from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated

from .models import (
    User, 
    Cargo, 
    Departamento, 
    Atributo, 
    DocumentoAtributo,
    ValorAtributo,
)

from .serializers import (
    UserSerializer,
    CargoSerializer,
    DepartamentoSerializer,
    AtributoSerializer,
    DocumentoAtributoSerializer,
    ValorAtributoSerializer,
)

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


class AtributoViewSet(viewsets.ModelViewSet):
    serializer_class = AtributoSerializer
    queryset = Atributo.objects.all()
    permission_classes = (DjangoModelPermissions,)


class DocumentoAtributoViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentoAtributoSerializer
    queryset = DocumentoAtributo.objects.all()
    permission_classes = (DjangoModelPermissions,)


class ValorAtributoViewSet(viewsets.ModelViewSet):
    serializer_class = ValorAtributoSerializer
    queryset = ValorAtributo.objects.all()
    permission_classes = (DjangoModelPermissions,)
