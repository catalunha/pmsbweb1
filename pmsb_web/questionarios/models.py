import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from core.mixins import UUIDModelMixin, UserOwnedModelMixin, TimedModelMixin

class Localizacao(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    altitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return "latitude: {} longitute:{} altitude:{}".format(self.latitude, self.longitude, self.altitude)

"""
    Class Questionario
    documentação
"""
class Questionario(UUIDModelMixin, UserOwnedModelMixin, TimedModelMixin):
    nome = models.CharField(max_length = 255)

    publicado = models.BooleanField(default = False)

    perguntas = models.ManyToManyField(
        "Pergunta",
        through = "PerguntaDoQuestionario",
        through_fields = ("questionario","pergunta"),
        related_name = "questionarios",
    )

    class Meta:
        verbose_name = "Questionario"
        verbose_name_plural = "Questionarios"

    def __str__(self):
        return "Questionario {}".format(self.nome)

class Pergunta(UUIDModelMixin, TimedModelMixin):

    TIPO_UNICA_ESCOLHA = 0
    TIPO_MULTIPLA_ESCOLHA = 1
    TIPO_TEXTO = 2
    TIPO_ARQUIVO = 3
    TIPO_IMAGEM = 4
    TIPO_COORDENADA = 5
    TIPO_NUMERO = 6

    TIPO_PERGUNTA_CHOICES = (
        (TIPO_UNICA_ESCOLHA, "Unica Escolha"),
        (TIPO_MULTIPLA_ESCOLHA, "Multipla Escolha"),
        (TIPO_TEXTO, "Texto"),
        (TIPO_ARQUIVO, "Arquivo"),
        (TIPO_IMAGEM, "Imagem"),
        (TIPO_COORDENADA, "Coordenada"),
        (TIPO_NUMERO, "Numero"),
    )

    variavel = models.CharField(max_length = 255)

    texto = models.TextField()
    
    tipo = models.PositiveSmallIntegerField(choices = TIPO_PERGUNTA_CHOICES)
    
    possivel_escolha_requisito = models.ForeignKey("PossivelEscolha", on_delete = models.SET_NULL, null = True, blank = True, related_name="pre_requisito_de")

    class Meta:
        ordering = ("tipo",)
        verbose_name = "Pergunta"
        verbose_name_plural = "Perguntas"

    def __str__(self):
        return "{} - {}: {}".format(self.tipo_texto(), self.variavel, self.texto)
    
    def tipo_texto(self):
        return self.TIPO_PERGUNTA_CHOICES[int(self.tipo)][1]

class PerguntaDoQuestionario(UUIDModelMixin, TimedModelMixin):
    questionario = models.ForeignKey(Questionario, on_delete = models.CASCADE)
    pergunta = models.ForeignKey(Pergunta, on_delete = models.CASCADE)
    ordem = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ("questionario", "pergunta")
        ordering = ("questionario","ordem","pergunta")


class PossivelEscolha(UUIDModelMixin, TimedModelMixin):
    pergunta = models.ForeignKey(Pergunta, on_delete = models.CASCADE, related_name="possiveis_escolhas")
    texto = models.TextField()

    class Meta:
        verbose_name = "Possivel Escolha"
        verbose_name_plural = "Possiveis Escolhas"

    def __str__(self):
        return "{0} -> {1}".format(self.pergunta, self.texto)

class RespostaQuestionario(UUIDModelMixin, UserOwnedModelMixin, TimedModelMixin):
    questionario = models.ForeignKey(Questionario, on_delete = models.CASCADE, related_name="respostas")
    objects = models.Manager()

    class Meta:
        verbose_name = "Resposta Questionario"
        verbose_name_plural = "Respostas Questionarios"

    def __str__(self):
        return "Resposta do {0}".format(self.questionario)

class RespostaPergunta(UUIDModelMixin, TimedModelMixin):
    resposta_questionario = models.ForeignKey(RespostaQuestionario, on_delete = models.CASCADE)
    pergunta = models.ForeignKey(Pergunta, on_delete = models.CASCADE)
    localizacao = models.ForeignKey(Localizacao, on_delete = models.CASCADE)

    class Meta:
        unique_together = ("resposta_questionario", "pergunta")
        verbose_name = "Resposta Pergunta"
        verbose_name_plural = "Respostas Perguntas"

    @property
    def tipo(self):
        return self.pergunta.tipo

    def set_resposta(self, instance):
        if self.tipo == "":
            pass
        
        if isinstance(instance, PossivelEscolhaResposta):
            pass


class PossivelEscolhaResposta(UUIDModelMixin, TimedModelMixin):
    resposta_pergunta = models.ForeignKey(RespostaPergunta, on_delete = models.CASCADE, related_name="escolhas")
    possivel_escolha = models.ForeignKey(PossivelEscolha, on_delete = models.CASCADE)

    class Meta:
        unique_together = ("resposta_pergunta", "possivel_escolha")

class CoordenadaResposta(UUIDModelMixin, TimedModelMixin):
    resposta_pergunta = models.ForeignKey(RespostaPergunta, on_delete = models.CASCADE, related_name="coordenadas")
    coordenada = models.ForeignKey(Localizacao, on_delete = models.CASCADE, null = True)

class TextoResposta(UUIDModelMixin, TimedModelMixin):
    resposta_pergunta = models.ForeignKey(RespostaPergunta, on_delete = models.CASCADE, related_name="textos")
    texto = models.TextField()

class NumeroResposta(UUIDModelMixin, TimedModelMixin):
    resposta_pergunta = models.ForeignKey(RespostaPergunta, on_delete = models.CASCADE, related_name="numeros")
    numero = models.IntegerField()

def caminho_para_arquivos(instance, filename):
    hoje = timezone.now()
    try:
        file_uuid = instance.id
    except:
        file_uuid = uuid.uuid4()
    
    nome_arquivo = "{0}_{1}".format(file_uuid, filename)
    return "questionarios/arquivos/{1}/{2}/{3}/{4}".format( hoje.year, hoje.month, hoje.day, nome_arquivo)

class ArquivoResposta(UUIDModelMixin, TimedModelMixin):
    resposta_pergunta = models.ForeignKey(RespostaPergunta, on_delete = models.CASCADE, related_name="arquivos")
    arquivo = models.FileField(upload_to=caminho_para_arquivos)

def caminho_para_imagens(instance, filename):
    hoje = timezone.now()
    try:
        file_uuid = instance.id
    except:
        file_uuid = uuid.uuid4()
    
    nome_arquivo = "{0}_{1}".format(file_uuid, filename)
    return "questionarios/imagens/{1}/{2}/{3}/{4}".format( hoje.year, hoje.month, hoje.day, nome_arquivo)

class ImagemResposta(UUIDModelMixin, TimedModelMixin):
    resposta_pergunta = models.ForeignKey(RespostaPergunta, on_delete = models.CASCADE, related_name="imagens")
    imagem = models.ImageField(upload_to=caminho_para_imagens)