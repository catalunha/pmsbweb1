from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers, viewsets, routers
from rest_framework import generics

from .models import (

    Localizacao,
    Questionario,
    
    Pergunta,
    PerguntaDoQuestionario,
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
    
    PerguntaRequisito,
    EscolhaRequisito,

    UnidadeMedida,

    PossivelEscolhaResposta,
    CoordenadaResposta,
    TextoResposta,
    NumeroResposta,
    ArquivoResposta,
    ImagemResposta,

)


User = get_user_model()

""" Requisitos """

class FakeDeleteListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(fake_deletado = False)
        return super().to_representation(data)

class FakeDeleteSerializerMeta:
    list_serializer_class = FakeDeleteListSerializer



class PerguntaDoQuestionarioSerializer(serializers.ModelSerializer):
    class Meta(FakeDeleteSerializerMeta):
        model = PerguntaDoQuestionario
        fields = ("id","questionario","pergunta")


class PerguntaRequisitoSerializer(serializers.ModelSerializer):

    pergunta_requisito = PerguntaDoQuestionarioSerializer()

    class Meta(FakeDeleteSerializerMeta):
        model = PerguntaRequisito
        fields = ( "id","pergunta_requisito")

class PerguntaRequisitoViewSet(viewsets.ModelViewSet):
    serializer_class = PerguntaRequisitoSerializer
    queryset = PerguntaRequisito.objects.all()



class EscolhaRequisitoSerializer(serializers.ModelSerializer):
    class Meta(FakeDeleteSerializerMeta):
        model = EscolhaRequisito
        fields = ("id","questionario","escolha_requisito")

class EscolhaRequisitoViewSet(viewsets.ModelViewSet):
    serializer_class = EscolhaRequisitoSerializer
    queryset = EscolhaRequisito.objects.all()



class LocalizacaoSerializer(serializers.ModelSerializer):
    class Meta(FakeDeleteSerializerMeta):
        model = Localizacao
        fields = ("id", "latitude", "longitude", "altitude")


class LocalizacaoViewSet(viewsets.ModelViewSet):
    serializer_class = LocalizacaoSerializer
    queryset = Localizacao.objects.all()


class UserSerializer(serializers.ModelSerializer):
    class Meta(FakeDeleteSerializerMeta):
        model = User
        fields = ("id", "username", "email")
    

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PossivelEscolhaSerializer(serializers.ModelSerializer):
    class Meta(FakeDeleteSerializerMeta):
        model = PossivelEscolha
        fields = ("id", "criado_em", "editado_em", "texto", "pergunta")

class PossivelEscolhaViewSet(viewsets.ModelViewSet):
    queryset = PossivelEscolha.objects.all()
    serializer_class = PossivelEscolhaSerializer

class PerguntaSerializerMixin(serializers.ModelSerializer):
    perguntarequisito_set = PerguntaRequisitoSerializer(many=True, read_only = True)
    escolharequisito_set = EscolhaRequisitoSerializer(many = True, read_only = True)
    class Meta(FakeDeleteSerializerMeta):
        model = Pergunta
        fields = (
            "id",
            "criado_em",
            "editado_em",
            "variavel",
            "texto",
            "tipo",
            "perguntarequisito_set",
            "escolharequisito_set",
        )


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
        fields = PerguntaSerializerMixin.Meta.fields + ("multipla", "possiveis_escolhas")

class PerguntaEscolhaViewSet(viewsets.ModelViewSet):
    queryset = PerguntaEscolha.objects.all()
    serializer_class = PerguntaEscolhaSerializer

class UnidadeMedidaSerializer(serializers.ModelSerializer):
    class Meta(FakeDeleteSerializerMeta):
        model = UnidadeMedida
        fields = ("id","nome","sigla")

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

class QuestionarioSerializer(serializers.ModelSerializer):
    usuario = UserSerializer()
    perguntas = serializers.SerializerMethodField()
    class Meta(FakeDeleteSerializerMeta):
        model = Questionario
        fields = ("id", "usuario", "nome", "criado_em", "editado_em", "publicado", "perguntas")
    
    def get_perguntas(self, instance):
        perguntas = instance.perguntas
        return PerguntaSerializer(perguntas, many = True, read_only = True).data

class QuestionarioViewSet(viewsets.ModelViewSet):
    queryset = Questionario.objects.all()
    serializer_class = QuestionarioSerializer


""" Respotas """


""" Respostas dos tipos """

class PossivelEscolhaRespostaSerializer(serializers.ModelSerializer):
    class Meta(FakeDeleteSerializerMeta):
        model = PossivelEscolhaResposta
        fields = "__all__"

class PossivelEscolhaRespostaViewSet(viewsets.ModelViewSet):
    serializer_class = PossivelEscolhaRespostaSerializer
    queryset = PossivelEscolhaResposta.objects.all()

class CoordenadaRespostaSerializer(serializers.ModelSerializer):
    coordenada = LocalizacaoSerializer()
    class Meta(FakeDeleteSerializerMeta):
        model = CoordenadaResposta
        fields = "__all__"
    
class CoordenadaRespostaViewSet(viewsets.ModelViewSet):
    serializer_class = CoordenadaRespostaSerializer
    queryset = CoordenadaResposta.objects.all()

class TextoRespostaSerializer(serializers.ModelSerializer):
    class Meta(FakeDeleteSerializerMeta):
        model = TextoResposta
        fields = "__all__"

class TextoRespostaViewSet(viewsets.ModelViewSet):
    serializer_class = TextoRespostaSerializer
    queryset = TextoResposta.objects.all()

class NumeroRespostaSerializer(serializers.ModelSerializer):
    class Meta(FakeDeleteSerializerMeta):
        model = NumeroResposta
        fields = "__all__"

class NumeroRespostaViewSet(viewsets.ModelViewSet):
    serializer_class = NumeroRespostaSerializer
    queryset = NumeroResposta.objects.all()

class ArquivoRespostaSerializer(serializers.ModelSerializer):
    class Meta(FakeDeleteSerializerMeta):
        model = ArquivoResposta
        fields = "__all__"

class ArquivoRespostaViewSet(viewsets.ModelViewSet):
    serializer_class = ArquivoRespostaSerializer
    queryset = ArquivoResposta.objects.all()

class ImagemRespostaSerializer(serializers.ModelSerializer):
    class Meta(FakeDeleteSerializerMeta):
        model = ImagemResposta
        fields = "__all__"

class ImagemRespostaViewSet(viewsets.ModelViewSet):
    serializer_class = ImagemRespostaSerializer
    queryset = ImagemResposta.objects.all()

""" Resposta Pergunta """

class RespostaPerguntaSerializer(serializers.ModelSerializer):
    pergunta = PerguntaSerializer
    localizacao = LocalizacaoSerializer(required = False)
    escolhas = PossivelEscolhaRespostaSerializer(many = True, required = False)
    coordenada = CoordenadaRespostaSerializer(required = False)
    texto = TextoRespostaSerializer(required = False)
    numero = NumeroRespostaSerializer(required = False)
    arquivo = ArquivoRespostaSerializer(required = False)
    imagem = ImagemRespostaSerializer(required = False)

    class Meta(FakeDeleteSerializerMeta):
        model = RespostaPergunta
        fields = (
            "id",
            "localizacao",
            "resposta_questionario",
            "pergunta",
            "tipo",
            "coordenada",
            "escolhas",
            "texto",
            "numero",
            "arquivo",
            "imagem",
        )

    
    def create(self, validated_data):

        localizacao_data = validated_data.pop("localizacao", None)

        #tipos de respostas
        coordenada_data = validated_data.pop("coordenada", None)
        imagem_data = validated_data.pop("imagem", None)
        arquivo_data = validated_data.pop("arquivo", None)
        numero_data = validated_data.pop("numero", None)
        texto_data = validated_data.pop("texto", None)
        escolhas_data = validated_data.pop("escolhas", None)
        
        resposta = RespostaPergunta.objects.create(**validated_data)
        
        if localizacao_data is not None:
            localizacao = LocalizacaoSerializer(data = localizacao_data)

            if localizacao.is_valid():
                localizacao.save()
        
        if coordenada_data is not None:
            coordenada = CoordenadaRespostaSerializer(data = coordenada_data)
            if coordenada.is_valid():
                coordenada.save()
        
        return resposta
        

class RespostaPerguntaViewSet(viewsets.ModelViewSet):
    queryset = RespostaPergunta.objects.all()
    serializer_class = RespostaPerguntaSerializer

""" Resposta Questionario """
class RespostaQuestionarioSerializer(serializers.ModelSerializer):
    perguntas = RespostaPerguntaSerializer(many = True, read_only = True)

    class Meta(FakeDeleteSerializerMeta):
        model = RespostaQuestionario
        fields = ("id",  "usuario", "setor_censitario", "questionario", "perguntas")

class RespostaQuestionarioViewSet(viewsets.ModelViewSet):
    queryset = RespostaQuestionario.objects.all()
    serializer_class = RespostaQuestionarioSerializer