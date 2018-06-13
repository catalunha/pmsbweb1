from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers, viewsets, routers
from .models import Questionario, Pergunta, PossivelEscolha

User = get_user_model()

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "sexo")

class QuestionarioSerializer(serializers.HyperlinkedModelSerializer):
    usuario = UserSerializer
    class Meta:
        model = Questionario
        fields = "__all__"


class PossivelEscolhaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PossivelEscolha
        fields = "__all__"

class PerguntaSerializer(serializers.HyperlinkedModelSerializer):
    possiveis_escolhas = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name="possivelescolha-detail")
    class Meta:
        model = Pergunta
        fields = "__all__"