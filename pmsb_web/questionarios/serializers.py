from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers, viewsets, routers
from rest_framework import generics
from .models import Questionario, Pergunta, PerguntaEscolha, PossivelEscolha
from .models import PerguntaArquivo, PerguntaCoordenada, PerguntaEscolha, PerguntaImagem, PerguntaNumero, PerguntaTexto
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
        fields = ("id", "url", "criado_em", "editado_em", "texto", "pergunta", "pre_requisito_de")
        extra_kwargs  = {"pergunta":{"view_name":"pergunta-detail"}}

class PossivelEscolhaViewSet(viewsets.ModelViewSet):
    queryset = PossivelEscolha.objects.all()
    serializer_class = PossivelEscolhaSerializer

class PerguntaSerializerMixin(serializers.HyperlinkedModelSerializer):
    possivel_escolha_requisito = serializers.PrimaryKeyRelatedField(read_only = True)
    class Meta:
        model = Pergunta
        fields = (
            "id",
            "url",
            "criado_em",
            "editado_em",
            "variavel",
            "texto",
            "tipo",
            "possivel_escolha_requisito",
        )

class PerguntaSerializer(PerguntaSerializerMixin):

    class Meta(PerguntaSerializerMixin):
        model = PerguntaSerializerMixin.Meta.model
        fields = PerguntaSerializerMixin.Meta.fields
    
    def to_representation(self, instance):
        if isinstance(instance, PerguntaEscolha):
            return PerguntaEscolhaSerializer(instance = instance, context = self.context).data
        elif isinstance(instance, PerguntaNumero):
            return PerguntaNumeroSerializer(instance = instance, context = self.context).data
        elif isinstance(instance, PerguntaArquivo):
            return PerguntaArquivoSerializer(instance = instance, context = self.context).data
        elif isinstance(instance, PerguntaTexto):
            return PerguntaTextoSerializer(instance = instance, context = self.context).data
        elif isinstance(instance, PerguntaCoordenada):
            return PerguntaCoordenadaSerializer(instance = instance, context = self.context).data
        elif isinstance(instance, PerguntaImagem):
            return PerguntaImagemSerializer(instance = instance, context = self.context).data
        elif isinstance(instance, Pergunta):
            return super(PerguntaSerializer, self).to_representation(instance)
        else:
            return None

class PerguntaEscolhaSerializer(serializers.ModelSerializer):
    #possiveis_escolhas = PossivelEscolhaSerializer(many = True, read_only = True)
    class Meta:
        model = PerguntaEscolha
        fields = "__all__"

class PerguntaNumeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerguntaNumero
        fields = "__all__"

class PerguntaArquivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerguntaArquivo
        fields = "__all__"

class PerguntaTextoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerguntaTexto
        fields = "__all__"

class PerguntaCoordenadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerguntaCoordenada
        fields = "__all__"
    
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