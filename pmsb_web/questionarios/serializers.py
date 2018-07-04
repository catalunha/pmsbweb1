from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers, viewsets, routers
from .models import Questionario, Pergunta, PossivelEscolha
from .models import RespostaQuestionario, RespostaPergunta, PossivelEscolhaResposta


User = get_user_model()

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PossivelEscolhaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PossivelEscolha
        fields = ("id", "url", "criado_em", "editado_em", "texto", "pergunta")

class PossivelEscolhaViewSet(viewsets.ModelViewSet):
    queryset = PossivelEscolha.objects.all()
    serializer_class = PossivelEscolhaSerializer

class PerguntaSerializer(serializers.HyperlinkedModelSerializer):
    possiveis_escolhas = PossivelEscolhaSerializer(many = True, read_only = True)
    possivel_escolha_requisito = serializers.PrimaryKeyRelatedField(read_only = True)
    tipo = serializers.SerializerMethodField()
    class Meta:
        model = Pergunta
        fields = ("id", "url","criado_em","editado_em","variavel","texto","tipo","possivel_escolha_requisito","possiveis_escolhas")
    
    def __init__(self, *args, **kwargs):
        super(PerguntaSerializer, self).__init__(*args, **kwargs)
    
    def get_tipo(self, obj):
        return obj.tipo

class PerguntasViewSet(viewsets.ModelViewSet):
    queryset = Pergunta.objects.all()
    serializer_class = PerguntaSerializer


class QuestionarioSerializer(serializers.HyperlinkedModelSerializer):
    usuario = UserSerializer
    perguntas = PerguntaSerializer(many = True, read_only = True)
    class Meta:
        model = Questionario
        fields = ("id", "url", "usuario", "nome", "criado_em", "editado_em", "publicado", "perguntas")

class QuestionarioViewSet(viewsets.ModelViewSet):
    queryset = Questionario.objects.all()
    serializer_class = QuestionarioSerializer

class RespostaPerguntaSerializer(serializers.ModelSerializer):
    pergunta = PerguntaSerializer
    conteudo = serializers.PrimaryKeyRelatedField(many = True, read_only = True)
    class Meta:
        model = RespostaPergunta
        fields = ("id", "url", "resposta_questionario", "pergunta", "tipo", "conteudo")

class RespostaPerguntaViewSet(viewsets.ModelViewSet):
    queryset = RespostaPergunta.objects.all()
    serializer_class = RespostaPerguntaSerializer

class RespostaQuestionarioSerializer(serializers.HyperlinkedModelSerializer):
    usuario = UserSerializer
    questionario = QuestionarioSerializer
    perguntas = RespostaPerguntaSerializer(many = True, read_only = True)
    class Meta:
        model = RespostaQuestionario
        fields = ("id", "url", "usuario", "questionario", "perguntas")


class RespostaQuestionarioViewSet(viewsets.ModelViewSet):
    queryset = RespostaQuestionario.objects.all()
    serializer_class = RespostaQuestionarioSerializer


class PossivelEscolhaRespostaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PossivelEscolhaResposta
        fields = "__all__"