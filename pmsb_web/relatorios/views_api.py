from rest_framework import viewsets
from relatorios.serializers import (
    RelatorioSerializer,
    BlocoSerializer,
    FiguraSerializer,
)
from relatorios.models import (
    Relatorio,
    Bloco,
    Figura,
)


class RelatorioViewset(viewsets.ModelViewSet):
    serializer_class = RelatorioSerializer
    queryset = Relatorio.objects.all()


class BlocoViewset(viewsets.ModelViewSet):
    serializer_class = BlocoSerializer
    queryset = Bloco.objects.all()


class FiguraViewset(viewsets.ModelViewSet):
    serializer_class = FiguraSerializer
    queryset = Figura.objects.all()