from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers, viewsets, routers
from .models import Questionario, Pergunta, PossivelEscolha

User = get_user_model()

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")

class PossivelEscolhaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PossivelEscolha
        fields = ("id", "url", "criado_em", "editado_em", "texto", "pergunta")

class PerguntaSerializer(serializers.HyperlinkedModelSerializer):
    #possiveis_escolhas = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name="possivelescolha-detail")
    possiveis_escolhas = PossivelEscolhaSerializer(many = True, read_only = True)
    possivel_escolha_requisito = serializers.PrimaryKeyRelatedField(read_only = True)
    class Meta:
        model = Pergunta
        fields = ("id", "url","possiveis_escolhas","criado_em","editado_em","variavel","texto","tipo","possivel_escolha_requisito")

class QuestionarioSerializer(serializers.HyperlinkedModelSerializer):
    usuario = UserSerializer
    perguntas = PerguntaSerializer(many = True, read_only = True)
    class Meta:
        model = Questionario
        fields = ("id", "url", "usuario", "nome", "criado_em", "editado_em", "publicado", "perguntas")