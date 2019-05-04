from core.mixins import ArquivoBase64SerializerField
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.validators import UniqueValidator

from .models import (

    Localizacao,
    Questionario,
    SetorCensitario,
    Pergunta,
    PerguntaDoQuestionario,
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
    Grupo,
)

User = get_user_model()


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class CreateListModelMixin(object):

    def get_serializer(self, *args, **kwargs):
        """ if an array is passed, set serializer to many """
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(CreateListModelMixin, self).get_serializer(*args, **kwargs)


""" Requisitos """


class FakeDeleteListSerializer(serializers.ListSerializer):
    def to_representation(self, data):

        try:
            data = data.filter(fake_deletado=False)
        except AttributeError as e:
            pass

        return super().to_representation(data)


class FakeDeleteSerializerMeta:
    list_serializer_class = FakeDeleteListSerializer


class PerguntaDoQuestionarioSerializer(serializers.ModelSerializer):
    class Meta(FakeDeleteSerializerMeta):
        model = PerguntaDoQuestionario
        fields = ("id", "questionario", "pergunta")


class PerguntaRequisitoSerializer(serializers.ModelSerializer):
    pergunta_requisito = PerguntaDoQuestionarioSerializer()

    class Meta(FakeDeleteSerializerMeta):
        model = PerguntaRequisito
        fields = ("id", "pergunta_requisito")


class PerguntaRequisitoViewSet(viewsets.ModelViewSet):
    serializer_class = PerguntaRequisitoSerializer
    queryset = PerguntaRequisito.objects.all()


class EscolhaRequisitoSerializer(serializers.ModelSerializer):
    pergunta = serializers.SerializerMethodField()

    class Meta(FakeDeleteSerializerMeta):
        model = EscolhaRequisito
        fields = ("id", "questionario", "pergunta", "escolha_requisito")

    def get_pergunta(self, instance):
        return instance.escolha_requisito.pergunta.pk


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
    class Meta:
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
    perguntarequisito_set = PerguntaRequisitoSerializer(
        many=True, read_only=True)
    escolharequisito_set = EscolhaRequisitoSerializer(
        many=True, read_only=True)

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
            return PerguntaEscolhaSerializer(instance=instance, context=self.context).data
        elif isinstance(instance, PerguntaNumero):
            return PerguntaNumeroSerializer(instance=instance, context=self.context).data
        elif isinstance(instance, PerguntaArquivo):
            return PerguntaArquivoSerializer(instance=instance, context=self.context).data
        elif isinstance(instance, PerguntaTexto):
            return PerguntaTextoSerializer(instance=instance, context=self.context).data
        elif isinstance(instance, PerguntaCoordenada):
            return PerguntaCoordenadaSerializer(instance=instance, context=self.context).data
        elif isinstance(instance, PerguntaImagem):
            return PerguntaImagemSerializer(instance=instance, context=self.context).data
        else:
            return super(PerguntaSerializer, self).to_representation(instance)


class PerguntasViewSet(viewsets.ModelViewSet):
    queryset = Pergunta.objects.all()
    serializer_class = PerguntaSerializer


class PerguntaEscolhaSerializer(PerguntaSerializerMixin):
    possiveis_escolhas = PossivelEscolhaSerializer(many=True, read_only=True)

    class Meta(PerguntaSerializerMixin.Meta):
        model = PerguntaEscolha
        fields = PerguntaSerializerMixin.Meta.fields + \
                 ("multipla", "possiveis_escolhas")


class PerguntaEscolhaViewSet(viewsets.ModelViewSet):
    queryset = PerguntaEscolha.objects.all()
    serializer_class = PerguntaEscolhaSerializer


class UnidadeMedidaSerializer(serializers.ModelSerializer):
    class Meta(FakeDeleteSerializerMeta):
        model = UnidadeMedida
        fields = ("id", "nome", "sigla")


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
        fields = ("id", "usuario", "grupo", "nome", "criado_em",
                  "editado_em", "publicado", "perguntas")

    def get_perguntas(self, instance):
        perguntas = instance.perguntas
        return PerguntaSerializer(perguntas, many=True, read_only=True).data


class QuestionarioViewSet(viewsets.ModelViewSet):
    queryset = Questionario.objects.all()
    serializer_class = QuestionarioSerializer


""" Respotas """

""" Respostas dos tipos """


class ExcludeFakeDeleteFieldsMeta:
    exclude = ("fake_deletado", "fake_deletado_em")


class PossivelEscolhaRespostaSerializer(serializers.ModelSerializer):
    possivel_escolha = PossivelEscolhaSerializer

    class Meta(FakeDeleteSerializerMeta, ExcludeFakeDeleteFieldsMeta):
        model = PossivelEscolhaResposta


class PossivelEscolhaRespostaViewSet(CreateListModelMixin, viewsets.ModelViewSet):
    serializer_class = PossivelEscolhaRespostaSerializer
    queryset = PossivelEscolhaResposta.objects.all()


class CoordenadaRespostaSerializer(serializers.ModelSerializer):
    coordenada = LocalizacaoSerializer

    class Meta(FakeDeleteSerializerMeta, ExcludeFakeDeleteFieldsMeta):
        model = CoordenadaResposta


class CoordenadaRespostaViewSet(CreateListModelMixin, viewsets.ModelViewSet):
    serializer_class = CoordenadaRespostaSerializer
    queryset = CoordenadaResposta.objects.all()


class TextoRespostaSerializer(serializers.ModelSerializer):
    class Meta(FakeDeleteSerializerMeta, ExcludeFakeDeleteFieldsMeta):
        model = TextoResposta


class TextoRespostaViewSet(CreateListModelMixin, viewsets.ModelViewSet):
    serializer_class = TextoRespostaSerializer
    queryset = TextoResposta.objects.all()


class NumeroRespostaSerializer(serializers.ModelSerializer):
    class Meta(FakeDeleteSerializerMeta, ExcludeFakeDeleteFieldsMeta):
        model = NumeroResposta


class NumeroRespostaViewSet(CreateListModelMixin, viewsets.ModelViewSet):
    serializer_class = NumeroRespostaSerializer
    queryset = NumeroResposta.objects.all()


class ArquivoRespostaSerializer(serializers.ModelSerializer):
    arquivo = ArquivoBase64SerializerField()

    class Meta(FakeDeleteSerializerMeta, ExcludeFakeDeleteFieldsMeta):
        model = ArquivoResposta


class ArquivoRespostaViewSet(CreateListModelMixin, viewsets.ModelViewSet):
    serializer_class = ArquivoRespostaSerializer
    queryset = ArquivoResposta.objects.all()


class ImagemRespostaSerializer(serializers.ModelSerializer):
    imagem = Base64ImageField()

    class Meta(FakeDeleteSerializerMeta, ExcludeFakeDeleteFieldsMeta):
        model = ImagemResposta


class ImagemRespostaViewSet(CreateListModelMixin, viewsets.ModelViewSet):
    serializer_class = ImagemRespostaSerializer
    queryset = ImagemResposta.objects.all()


""" Resposta Pergunta """


class RespostaPerguntaSerializer(serializers.ModelSerializer):
    localizacao = LocalizacaoSerializer(allow_null=True)
    tipo = serializers.SerializerMethodField()

    class Meta(FakeDeleteSerializerMeta):
        model = RespostaPergunta
        fields = (
            "id",
            "localizacao",
            "resposta_questionario",
            "pergunta",
            "tipo",
        )

    def get_tipo(self, instance):
        return instance.pergunta.tipo

    def create(self, validated_data):
        localizacao = validated_data.pop("localizacao")
        local = LocalizacaoSerializer(data=localizacao)
        if local.is_valid():
            local.save()
            validated_data["localizacao"] = local.instance
        return super().create(validated_data)


class RespostaPerguntaExpandidoSerializer(serializers.ModelSerializer):
    localizacao = LocalizacaoSerializer(allow_null=True)
    pergunta = PerguntaSerializer()
    resposta = serializers.SerializerMethodField()
    tipo = serializers.SerializerMethodField()

    class Meta(FakeDeleteSerializerMeta):
        model = RespostaPergunta
        fields = (
            "id",
            "localizacao",
            "resposta_questionario",
            "pergunta",
            "tipo",
            "resposta",
        )

    def get_resposta(self, instance):

        if instance.tipo == 0:
            return PossivelEscolhaRespostaSerializer(instance.escolhas, many=True).data
        elif instance.tipo == 1:
            try:
                return TextoRespostaSerializer(instance.texto).data
            except ObjectDoesNotExist:
                return None

        elif instance.tipo == 2:
            try:
                return ArquivoRespostaSerializer(instance.arquivo).data
            except ObjectDoesNotExist:
                return None

        elif instance.tipo == 3:
            try:
                return ImagemRespostaSerializer(instance.imagem).data
            except ObjectDoesNotExist:
                return None

        elif instance.tipo == 4:
            try:
                return CoordenadaRespostaSerializer(instance.coordenada).data
            except ObjectDoesNotExist:
                return None

        elif instance.tipo == 5:
            try:
                return NumeroRespostaSerializer(instance.numero).data
            except ObjectDoesNotExist:
                return None

    def get_tipo(self, instance):
        return instance.pergunta.tipo

    def create(self, validated_data):
        localizacao = validated_data.pop("localizacao")
        local = LocalizacaoSerializer(data=localizacao)
        if local.is_valid():
            local.save()
            validated_data["localizacao"] = local.instance
        return super().create(validated_data)


class RespostaPerguntaViewSet(CreateListModelMixin, viewsets.ModelViewSet):
    queryset = RespostaPergunta.objects.all()
    serializer_class = RespostaPerguntaSerializer
    # pagination_class = StandardResultsSetPagination


""" Resposta Questionario """


class RespostaQuestionarioSerializer(serializers.ModelSerializer):
    perguntas = RespostaPerguntaSerializer(many=True, read_only=True)

    class Meta:
        model = RespostaQuestionario
        fields = ("id", "usuario", "setor_censitario",
                  "questionario", "perguntas")


class RespostaQuestionarioViewSet(CreateListModelMixin, viewsets.ModelViewSet):
    queryset = RespostaQuestionario.objects.all()
    serializer_class = RespostaQuestionarioSerializer
    # pagination_class = StandardResultsSetPagination


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class SetorCensitarioExpandidoSerializer(serializers.ModelSerializer):
    subsetores = RecursiveField(many=True)

    class Meta:
        model = SetorCensitario
        fields = (
            "id",
            "criado_em",
            "editado_em",
            "fake_deletado",
            "fake_deletado_em",
            "nome",
            "ativo",
            "setor_superior",
            "subsetores",
        )


def strboolornone(str):
    if str == 'True':
        return True
    elif str == 'False':
        return False
    else:
        return None


class SetorCensitorioQueryset(object):
    def get_queryset(self):
        queryset = super().get_queryset()

        ativo = self.request.query_params.get('ativo', None)
        ativo = strboolornone(ativo)
        if ativo is not None:
            queryset = queryset.filter(ativo=ativo)

        return queryset


class SetorCensitarioExpandidoViewset(SetorCensitorioQueryset, viewsets.ModelViewSet):
    serializer_class = SetorCensitarioExpandidoSerializer
    queryset = SetorCensitario.objects.filter(setor_superior=None)


class SetorCensitarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetorCensitario
        fields = "__all__"
        extra_kwargs = {
            'id': {
                'read_only': False,
                'required': False,
                'validators': [UniqueValidator(queryset=SetorCensitario.objects.all()), ],
            }
        }


class SetorCensitarioViewset(SetorCensitorioQueryset, viewsets.ModelViewSet):
    serializer_class = SetorCensitarioSerializer
    queryset = SetorCensitario.objects.all()


class GrupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grupo
        fields = "__all__"


class GrupoViewset(viewsets.ModelViewSet):
    serializer_class = GrupoSerializer
    queryset = Grupo.objects.all()
