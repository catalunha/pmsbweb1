from rest_framework import viewsets
from relatorios.serializers import (
    RelatorioSerializer,
    BlocoSerializer,
    EditorSerializer,
    FiguraSerializer,
)
from relatorios.models import (
    Relatorio,
    Bloco,
    Editor,
    Figura,
)


class RelatorioViewset(viewsets.ModelViewSet):
    serializer_class = RelatorioSerializer
    queryset = Relatorio.objects.all()


class BlocoViewset(viewsets.ModelViewSet):
    serializer_class = BlocoSerializer
    queryset = Bloco.objects.all()


class EditorViewset(viewsets.ModelViewSet):
    serializer_class = EditorSerializer
    queryset = Editor.objects.all()


class FiguraViewset(viewsets.ModelViewSet):
    serializer_class = FiguraSerializer
    queryset = Figura.objects.all()