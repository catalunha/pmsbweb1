import uuid

from core.mixins import (
    UUIDModelMixin,
    FakeDeleteModelMixin,
    UserOwnedModelMixin,
    TimedModelMixin,
)
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from model_utils.managers import InheritanceManager

User = get_user_model()


class Localizacao(UUIDModelMixin, FakeDeleteModelMixin):
    """
    Localização: Localização em latitude, longitude e altitude que pode ser utilizada
    em respostas ou em qualquer ação do sistema
    """
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    altitude = models.DecimalField(max_digits=9, decimal_places=6)

    objects = models.Manager()

    class Meta:
        verbose_name = "Localização"
        verbose_name_plural = "Localizações"

    def __str__(self):
        return "latitude:{} longitute:{} altitude:{}".format(self.latitude, self.longitude, self.altitude)


"""
    Class Questionario
    documentação
"""


class QuestionarioManager(models.Manager):
    """
    QuestionarioManager: Gerenciados de querys para o modelo Questionario
    """

    def get_by_superior(self, usuario_superior):
        """
        :param usuario_superior:
        :return: Todos os questionarios de usuarios subordinados ao usuario_superior
        """
        queryset = self.get_queryset()
        todos_subordinados = list()
        subordinados = list()
        processados = list()

        for usuario in User.objects.filter(superior=usuario_superior):
            subordinados.append(usuario)

        while len(subordinados) > 0:
            a = subordinados.pop(0)
            processados.append(a)
            todos_subordinados.append(a)
            subsubordinados = User.objects.filter(superior=a)

            for subsubordinado in subsubordinados:
                if subsubordinado not in processados:
                    subordinados.append(subsubordinado)
        q = queryset.filter(usuario__in=todos_subordinados, fake_deletado=False)

        return q


class Grupo(UUIDModelMixin, FakeDeleteModelMixin, TimedModelMixin):
    nome = models.CharField(max_length=255, unique=True)
    descricao = models.TextField()

    def __str__(self):
        return self.nome


class Questionario(UUIDModelMixin, FakeDeleteModelMixin, UserOwnedModelMixin, TimedModelMixin):
    """
    Questionario: Representação do questionario
    """
    nome = models.CharField(max_length=255)
    grupo = models.ForeignKey(Grupo, on_delete=models.SET_NULL, null=True, blank=True)
    publicado = models.BooleanField(default=False)
    objects = QuestionarioManager()

    class Meta:
        ordering = ('nome',)
        verbose_name = "Questionario"
        verbose_name_plural = "Questionarios"

    def __str__(self):
        return "Questionario {}".format(self.nome)

    @property
    def perguntas_do_questionario(self):
        """
        :return: Lista de PerguntaDoQuestionario
        """
        return PerguntaDoQuestionario.objects.filter(questionario=self, fake_deletado=False)

    @property
    def perguntas(self):
        """
        :return: Lista de Pergunta
        """
        queryset = Pergunta.objects.filter(
            perguntadoquestionario__questionario=self,
            perguntadoquestionario__fake_deletado=False,
            fake_deletado=False,
        ).order_by(
            "perguntadoquestionario__ordem")
        return queryset


class PerguntaManger(models.Manager):
    """
    PerguntaManger: Gerenciador de querys para o modelo Pergunta
    """

    def by_questionario(self, questionario, exclude_obj=None):
        queryset = self.get_queryset().filter(perguntadoquestionario__questionario=questionario, fake_deletado=False)
        if exclude_obj is not None:
            queryset = queryset.exclude(pk=exclude_obj.pk)
        return queryset


class Pergunta(UUIDModelMixin, FakeDeleteModelMixin, UserOwnedModelMixin, TimedModelMixin):
    """
    Pergunta: Representação da pergunta
    """
    TIPO = None
    TIPO_VERBOSE = None
    variavel = models.CharField(max_length=255)
    texto = models.TextField()
    tipo = models.PositiveSmallIntegerField(editable=False)
    pergunta_requisito = models.ForeignKey("Pergunta", on_delete=models.SET_NULL, null=True, blank=True,
                                           related_name="pre_requisito_de")

    possivel_escolha_requisito = models.ForeignKey("PossivelEscolha", on_delete=models.SET_NULL, null=True, blank=True,
                                                   related_name="pre_requisito_de")

    objects = PerguntaManger()
    inherited_objects = InheritanceManager()

    class Meta:
        ordering = ("tipo",)
        verbose_name = "Pergunta"
        verbose_name_plural = "Perguntas"

    def __str__(self):
        return "{}".format(self.variavel)

    def save(self, *args, **kwargs):
        if self.tipo is None:
            self.tipo = self.TIPO
        super(Pergunta, self).save(*args, **kwargs)

        # atualiza editado_em nos questionarios com esta pergunta
        for perguntadoquestionario in self.perguntadoquestionario_set.all():
            perguntadoquestionario.questionario.save()

    @property
    def verbose_name_tipo(self):

        if self.tipo == PerguntaEscolha.TIPO:
            return PerguntaEscolha.TIPO_VERBOSE
        elif self.tipo == PerguntaTexto.TIPO:
            return PerguntaTexto.TIPO_VERBOSE
        elif self.tipo == PerguntaCoordenada.TIPO:
            return PerguntaCoordenada.TIPO_VERBOSE
        elif self.tipo == PerguntaArquivo.TIPO:
            return PerguntaArquivo.TIPO_VERBOSE
        elif self.tipo == PerguntaImagem.TIPO:
            return PerguntaImagem.TIPO_VERBOSE
        elif self.tipo == PerguntaNumero.TIPO:
            return PerguntaNumero.TIPO_VERBOSE

    def cast(self):
        if self.tipo == PerguntaEscolha.TIPO:
            return self.perguntaescolha
        elif self.tipo == PerguntaTexto.TIPO:
            return self.perguntatexto
        elif self.tipo == PerguntaCoordenada.TIPO:
            return self.perguntacoordenada
        elif self.tipo == PerguntaArquivo.TIPO:
            return self.perguntaarquivo
        elif self.tipo == PerguntaImagem.TIPO:
            return self.perguntaimagem
        elif self.tipo == PerguntaNumero.TIPO:
            return self.perguntanumero

    @property
    def possiveis_escolhas_fake_delete(self):
        return self.possiveis_escolhas.filter(fake_deletado=False)

    @property
    def escolharequisito_set_fake_delete(self):
        return self.escolharequisito_set.filter(fake_deletado=False)

    @property
    def perguntarequisito_set_fake_delete(self):
        return self.perguntarequisito_set.filter(fake_deletado=False)


class UnidadeMedida(UUIDModelMixin, FakeDeleteModelMixin):
    """
    Unidade de Medida: modelo representa unidades de medida utilizados em respostas numericas
    """
    nome = models.CharField(max_length=255, unique=True)
    sigla = models.CharField(max_length=25, unique=True)

    objects = models.Manager()

    class Meta:
        verbose_name = "Unidade de Medida"
        verbose_name_plural = "Unidades de Medida"
        ordering = ("nome", "sigla")

    def __str__(self):
        return "{} ({})".format(self.nome, self.sigla)


class PerguntaEscolha(Pergunta):
    TIPO = 0
    TIPO_VERBOSE = "Pergunta Escolha"
    multipla = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Pergunta Escolha"
        verbose_name_plural = "Perguntas Escolha"

    @property
    def multipla_verbose(self):
        if self.multipla:
            return "Multipla"
        else:
            return "Unica"

    @property
    def verbose_name_tipo(self):
        return f"{super().verbose_name_tipo} {self.multipla_verbose}"


class PerguntaTexto(Pergunta):
    TIPO = 1
    TIPO_VERBOSE = "Pergunta Texto"

    class Meta:
        verbose_name = "Pergunta Texto"
        verbose_name_plural = "Perguntas Texto"


class PerguntaArquivo(Pergunta):
    TIPO = 2
    TIPO_VERBOSE = "Pergunta Arquivo"

    class Meta:
        verbose_name = "Pergunta Arquivo"
        verbose_name_plural = "Perguntas Arquivo"


class PerguntaImagem(Pergunta):
    TIPO = 3
    TIPO_VERBOSE = "Pergunta Imagem"

    class Meta:
        verbose_name = "Pergunta Imagem"
        verbose_name_plural = "Perguntas Imagem"


class PerguntaCoordenada(Pergunta):
    TIPO = 4
    TIPO_VERBOSE = "Pergunta Coordenada"

    class Meta:
        verbose_name = "Pergunta Coordenada"
        verbose_name_plural = "Perguntas Coordenada"


class PerguntaNumero(Pergunta):
    TIPO = 5
    TIPO_VERBOSE = "Pergunta Numero"
    unidade_medida = models.ForeignKey(UnidadeMedida, on_delete=models.CASCADE)
    maior_que = models.FloatField(blank=True, null=True)
    menor_que = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = "Pergunta Numero"
        verbose_name_plural = "Perguntas Numero"


class PerguntaDoQuestionario(UUIDModelMixin, FakeDeleteModelMixin, TimedModelMixin):
    questionario = models.ForeignKey(Questionario, on_delete=models.CASCADE)
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    ordem = models.PositiveSmallIntegerField()

    objects = models.Manager()

    class Meta:
        unique_together = ("questionario", "pergunta")
        ordering = ("questionario", "ordem", "pergunta")
        verbose_name = "Pergunta do Questionario"
        verbose_name_plural = "Perguntas dos Questionarios"

    def __str__(self):
        return "{} - {}".format(self.questionario, self.pergunta)

    def save(self, *args, **kwargs):
        if self.ordem is None:
            queryset = PerguntaDoQuestionario.objects.filter(questionario=self.questionario)
            ultimo = queryset.last()

            if ultimo is None:
                self.ordem = 1
            else:
                self.ordem = ultimo.ordem + 1

        super(PerguntaDoQuestionario, self).save(*args, **kwargs)


class PossivelEscolha(UUIDModelMixin, FakeDeleteModelMixin, TimedModelMixin):
    pergunta = models.ForeignKey(PerguntaEscolha, on_delete=models.CASCADE, related_name="possiveis_escolhas")
    texto = models.TextField()

    objects = models.Manager()

    class Meta:
        verbose_name = "Possivel Escolha"
        verbose_name_plural = "Possiveis Escolhas"

    def __str__(self):
        return "{0} -> {1}".format(self.pergunta, self.texto)

    @classmethod
    def by_questionario(cls, questionario, exclude_pergunta=None):
        escolhas = PossivelEscolha.objects.filter(pergunta__in=questionario.perguntas.all())
        if exclude_pergunta and isinstance(exclude_pergunta, PerguntaEscolha):
            escolhas = escolhas.exclude(pergunta=exclude_pergunta)
        return escolhas


class PerguntaRequisito(UUIDModelMixin, FakeDeleteModelMixin, TimedModelMixin):
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    pergunta_requisito = models.ForeignKey(PerguntaDoQuestionario, on_delete=models.CASCADE)

    objects = models.Manager()

    class Meta:
        unique_together = ("pergunta", "pergunta_requisito")

    def __str__(self):
        return "{}".format(self.pergunta_requisito)


class EscolhaRequisito(UUIDModelMixin, FakeDeleteModelMixin, TimedModelMixin):
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    questionario = models.ForeignKey(Questionario, on_delete=models.CASCADE)
    escolha_requisito = models.ForeignKey(PossivelEscolha, on_delete=models.CASCADE)

    objects = models.Manager()

    class Meta:
        unique_together = ("pergunta", "questionario", "escolha_requisito")

    def __str__(self):
        return "{} - {}".format(self.questionario, self.escolha_requisito)


class SetorCensitario(UUIDModelMixin, FakeDeleteModelMixin, TimedModelMixin):
    nome = models.CharField(max_length=255)
    setor_superior = models.ForeignKey("SetorCensitario", null=True, blank=True, on_delete=models.SET_NULL,
                                       related_name="subsetores")
    ativo = models.BooleanField(default=True)

    objects = models.Manager()

    class Meta:
        ordering = ('nome',)
        unique_together = ("nome", "setor_superior")

    def __str__(self):
        if self.setor_superior is not None:
            return "{} -> {}".format(self.setor_superior, self.nome)
        else:
            return "{}".format(self.nome)


class RespostaQuestionario(UUIDModelMixin, FakeDeleteModelMixin, UserOwnedModelMixin, TimedModelMixin):
    setor_censitario = models.ForeignKey(SetorCensitario, on_delete=models.CASCADE, related_name="respostas")
    questionario = models.ForeignKey(Questionario, on_delete=models.CASCADE, related_name="respostas")
    objects = models.Manager()

    class Meta:
        verbose_name = "Resposta Questionario"
        verbose_name_plural = "Respostas Questionarios"
        unique_together = ("setor_censitario", "questionario")

    def __str__(self):
        return "Resposta do {0}".format(self.questionario)

    @property
    def to_csv(self, separador=','):
        csv_str = f"Grupo{separador} Aplicado na Área{separador}"
        csv_str += f"Questionario{separador} "
        csv_str += f"RespostaQuestionario{separador} "
        csv_str += f"Usuario{separador} Questionario Criado Em{separador} Questionario Editado Em{separador} Tipo{separador} "
        csv_str += f"Variavel{separador} "
        csv_str += f"Texto{separador} "
        csv_str += f"Criado Em{separador} "
        csv_str += f"Editado Em{separador} "
        csv_str += f"Localização{separador} "
        csv_str += f"Resposta{separador} "
        return csv_str


class RespostaPergunta(UUIDModelMixin, FakeDeleteModelMixin, TimedModelMixin):
    resposta_questionario = models.ForeignKey(RespostaQuestionario, on_delete=models.CASCADE, related_name="perguntas")
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    localizacao = models.ForeignKey(Localizacao, on_delete=models.CASCADE, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        unique_together = ("resposta_questionario", "pergunta")
        verbose_name = "Resposta da Pergunta"
        verbose_name_plural = "Respostas das Perguntas"

    def __str__(self):
        return "{} - {}".format(self.resposta_questionario, self.pergunta)

    @property
    def tipo(self):
        return self.pergunta.tipo

    @property
    def questionario(self):
        return self.resposta_questionario.questionario

    @property
    def grupo(self):
        return self.questionario.grupo

    @property
    def usuario(self):
        return self.resposta_questionario.usuario

    @property
    def setor_censitario(self):
        return self.resposta_questionario.setor_censitario

    @property
    def resposta(self):
        resposta_str = ""
        virgula = ';'
        if self.tipo == 0:
            for escolha in self.escolhas.all():
                resposta_str += f"{escolha.texto()}{virgula} "
        elif self.tipo == 1:
            if self.texto:
                resposta_str = f"{self.texto.texto}"

        elif self.tipo == 2:
            if self.arquivo:
                resposta_str = f"{self.arquivo.arquivo.url}"

        elif self.tipo == 3:
            if self.imagem:
                resposta_str = f"{self.imagem.imagem.url}"

        elif self.tipo == 4:
            if self.coordenada:
                resposta_str = f"{self.coordenada.coordenada}"

        elif self.tipo == 5:
            if self.numero:
                resposta_str = f"{self.numero.numero}"

        return resposta_str

    def to_csv(self, separador=','):
        csv_str = ""
        csv_str += f"{self.grupo}{separador} "
        csv_str += f"{self.setor_censitario}{separador} "
        csv_str += f"{self.questionario}{separador} "
        csv_str += f"{self.resposta_questionario.pk}{separador} "
        csv_str += f"{self.usuario}{separador} "
        csv_str += f"{self.questionario.criado_em}{separador} "
        csv_str += f"{self.questionario.editado_em}{separador} "

        csv_str += f"{self.pergunta.cast().verbose_name_tipo}{separador} "

        csv_str += f"{self.pergunta.variavel}{separador} "
        csv_str += f"{self.pergunta.texto}{separador} "
        csv_str += f"{self.criado_em}{separador} "
        csv_str += f"{self.editado_em}{separador} "
        csv_str += f"{self.localizacao}{separador} "

        csv_str += f"{self.resposta}{separador} "
        return csv_str


class PossivelEscolhaResposta(UUIDModelMixin, FakeDeleteModelMixin, TimedModelMixin):
    resposta_pergunta = models.ForeignKey(RespostaPergunta, on_delete=models.CASCADE, related_name="escolhas")
    possivel_escolha = models.ForeignKey(PossivelEscolha, on_delete=models.CASCADE)

    objects = models.Manager()

    class Meta:
        verbose_name = "Possivel Escolha Resposta"
        verbose_name_plural = "Possiveis Escolhas Resposta"
        unique_together = ("resposta_pergunta", "possivel_escolha")

    def texto(self):
        return self.possivel_escolha.texto


class CoordenadaResposta(UUIDModelMixin, FakeDeleteModelMixin, TimedModelMixin):
    resposta_pergunta = models.OneToOneField(RespostaPergunta, on_delete=models.CASCADE, related_name="coordenada")
    coordenada = models.ForeignKey(Localizacao, on_delete=models.CASCADE, null=True)

    objects = models.Manager()

    class Meta:
        verbose_name = "Coordenada Resposta"
        verbose_name_plural = "Coordenadas Resposta"
        unique_together = ("resposta_pergunta", "coordenada")


class TextoResposta(UUIDModelMixin, FakeDeleteModelMixin, TimedModelMixin):
    resposta_pergunta = models.OneToOneField(RespostaPergunta, on_delete=models.CASCADE, related_name="texto")
    texto = models.TextField()

    objects = models.Manager()

    class Meta:
        verbose_name = "Texto Resposta"
        verbose_name_plural = "Textos Resposta"


class NumeroResposta(UUIDModelMixin, FakeDeleteModelMixin, TimedModelMixin):
    resposta_pergunta = models.OneToOneField(RespostaPergunta, on_delete=models.CASCADE, related_name="numero")
    unidade_medida = models.ForeignKey(UnidadeMedida, on_delete=models.CASCADE)
    numero = models.FloatField()

    objects = models.Manager()

    class Meta:
        verbose_name = "Numero Resposta"
        verbose_name_plural = "Numeros Resposta"


def caminho_para_arquivos(instance, filename):
    hoje = timezone.now()
    try:
        file_uuid = instance.id
    except:
        file_uuid = uuid.uuid4()

    nome_arquivo = "{}_{}".format(file_uuid, filename)
    return "questionarios/arquivos/{}/{}/{}/{}".format(hoje.year, hoje.month, hoje.day, nome_arquivo)


class ArquivoResposta(UUIDModelMixin, FakeDeleteModelMixin, TimedModelMixin):
    resposta_pergunta = models.OneToOneField(RespostaPergunta, on_delete=models.CASCADE, related_name="arquivo")
    arquivo = models.FileField(upload_to=caminho_para_arquivos)

    objects = models.Manager()

    class Meta:
        verbose_name = "Arquivo Resposta"
        verbose_name_plural = "Arquivos Resposta"


def caminho_para_imagens(instance, filename):
    hoje = timezone.now()
    try:
        file_uuid = instance.id
    except:
        file_uuid = uuid.uuid4()

    nome_arquivo = "{}_{}".format(file_uuid, filename)
    return "questionarios/imagens/{}/{}/{}/{}".format(hoje.year, hoje.month, hoje.day, nome_arquivo)


class ImagemResposta(UUIDModelMixin, FakeDeleteModelMixin, TimedModelMixin):
    resposta_pergunta = models.OneToOneField(RespostaPergunta, on_delete=models.CASCADE, related_name="imagem")
    imagem = models.ImageField(upload_to=caminho_para_imagens)

    objects = models.Manager()

    class Meta:
        verbose_name = "Imagem Resposta"
        verbose_name_plural = "Imagens Resposta"
