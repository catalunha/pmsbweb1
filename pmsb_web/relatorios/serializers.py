from rest_framework import serializers
from relatorios.models import (
    Relatorio,
    Bloco,
    Editor,
    Figura,
)


class RelatorioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relatorio
        fields = "__all__"


class BlocoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bloco
        fields = "__all__"


class EditorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Editor
        fields = "__all__"


class FiguraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Figura
        fields = "__all__"