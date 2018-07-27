from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers, viewsets, routers
from rest_framework import generics
from .models import (
    Questionario,
    Pergunta,
    PerguntaEscolha,
    PossivelEscolha,
    PerguntaArquivo,
    PerguntaCoordenada,
    PerguntaEscolha,
    PerguntaImagem,
    PerguntaNumero,
    PerguntaTexto,
    RespostaQuestionario,
    RespostaPergunta,
    PossivelEscolhaResposta,
    UnidadeMedida,
)


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
    possivel_escolha_requisito = PossivelEscolhaSerializer()
    #possivel_escolha_requisito = serializers.SerializerMethodField()
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
    
    """
    def get_possivel_escolha_requisito(self, instance):
        print("sjaflskdjflajsdlfjla")
        return {
            "id": instance.possivel_escolha_requisito.id,
            "pergunta": instance.possivel_escolha_requisito.pergunta,
        }
    """


class PerguntaSerializer(PerguntaSerializerMixin):

    class Meta(PerguntaSerializerMixin.Meta):
        pass
    
    def to_representation(self, instance):
        instance = instance.cast()
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
        else:
            return super(PerguntaSerializer, self).to_representation(instance)


class PerguntasViewSet(viewsets.ModelViewSet):
    queryset = Pergunta.objects.all()
    serializer_class = PerguntaSerializer

class PerguntaEscolhaSerializer(PerguntaSerializerMixin):
    possiveis_escolhas = PossivelEscolhaSerializer(many=True, read_only = True)
    class Meta(PerguntaSerializerMixin.Meta):
        model = PerguntaEscolha
        fields = "__all__"

class PerguntaEscolhaViewSet(viewsets.ModelViewSet):
    queryset = PerguntaEscolha.objects.all()
    serializer_class = PerguntaEscolhaSerializer

class UnidadeMedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadeMedida
        fields = "__all__"

class PerguntaNumeroSerializer(PerguntaSerializerMixin):
    unidade_medida = UnidadeMedidaSerializer(read_only=True)
    class Meta(PerguntaSerializerMixin.Meta):
        model = PerguntaNumero
        fields = "__all__"

class PerguntaNumeroViewSet(viewsets.ModelViewSet):
    queryset = PerguntaNumero.objects.all()
    serializer_class = PerguntaNumeroSerializer

class PerguntaArquivoSerializer(PerguntaSerializerMixin):
    class Meta(PerguntaSerializerMixin.Meta):
        model = PerguntaArquivo
        fields = "__all__"

class PerguntaArquivoViewSet(viewsets.ModelViewSet):
    queryset = PerguntaArquivo.objects.all()
    serializer_class = PerguntaArquivoSerializer

class PerguntaTextoSerializer(PerguntaSerializerMixin):
    class Meta(PerguntaSerializerMixin.Meta):
        model = PerguntaTexto
        fields = "__all__"

class PerguntaTextoViewSet(viewsets.ModelViewSet):
    queryset = PerguntaTexto.objects.all()
    serializer_class = PerguntaTextoSerializer

class PerguntaCoordenadaSerializer(PerguntaSerializerMixin):
    class Meta(PerguntaSerializerMixin.Meta):
        model = PerguntaCoordenada
        fields = "__all__"

class PerguntaCoordenadaViewSet(viewsets.ModelViewSet):
    queryset = PerguntaCoordenada.objects.all()
    serializer_class = PerguntaCoordenadaSerializer

class PerguntaImagemSerializer(PerguntaSerializerMixin):
    class Meta(PerguntaSerializerMixin.Meta):
        model = PerguntaImagem
        fields = "__all__"

class PerguntaImagemViewSet(viewsets.ModelViewSet):
    queryset = PerguntaImagem.objects.all()
    serializer_class = PerguntaImagemSerializer

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