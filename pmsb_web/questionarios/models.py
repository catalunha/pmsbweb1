import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from core.mixins import UUIDModelMixin, UserOwnedModelMixin, TimedModelMixin

class Localizacao(models.Model):
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
class Questionario(UUIDModelMixin, UserOwnedModelMixin, TimedModelMixin):
    nome = models.CharField(max_length = 255)

    publicado = models.BooleanField(default = False)

    perguntas = models.ManyToManyField(
        "Pergunta",
        through = "PerguntaDoQuestionario",
        through_fields = ("questionario","pergunta"),
        related_name = "questionarios",
    )

    objects = models.Manager()

    class Meta:
        verbose_name = "Questionario"
        verbose_name_plural = "Questionarios"

    def __str__(self):
        return "Questionario {}".format(self.nome)

class Pergunta(UUIDModelMixin, TimedModelMixin):

    # tipo default = 0, Unica Escolha
    TIPO = None

    variavel = models.CharField(max_length = 255)

    texto = models.TextField()
    
    tipo = models.PositiveSmallIntegerField(editable = False)
    
    possivel_escolha_requisito = models.ForeignKey("PossivelEscolha", on_delete = models.SET_NULL, null = True, blank = True, related_name="pre_requisito_de")

    objects = models.Manager()

    class Meta:
        ordering = ("tipo",)
        verbose_name = "Pergunta"
        verbose_name_plural = "Perguntas"

    def __str__(self):
        return "{}: {}".format(self.variavel, self.texto)
    
    def save(self, *args, **kwargs):
        self.tipo = self.TIPO
        super(Pergunta, self).save(*args, **kwargs)

class UnidadeMedida(models.Model):
    """
    Tabela - Unidade de Medida
    """
    nome = models.CharField(max_length = 255, unique = True)
    sigla = models.CharField(max_length = 5, unique = True)

    objects = models.Manager()

    class Meta:
        verbose_name = "Unidade de Medida"
        verbose_name_plural = "Unidades de Medida"
        ordering = ("nome", "sigla")
    
    def __str__(self):
        return "{} ({})".format(self.nome, self.sigla)


class PerguntaUnicaEscolha(Pergunta):
    TIPO = 0
    multipla = models.BooleanField(defalt = False)

    class Meta:
        verbose_name = "Pergunta Unica Escolha"
        verbose_name_plural = "Perguntas Unica Escolha"

class PerguntaMultiplaEscolha(Pergunta):
    TIPO = 1

    class Meta:
        verbose_name = "Pergunta Multipla Escolha"
        verbose_name_plural = "Perguntas Multipla Escolha"

class PerguntaTexto(Pergunta):
    TIPO = 2

    class Meta:
        verbose_name = "Pergunta Texto"
        verbose_name_plural = "Perguntas Texto"

class PerguntaArquivo(Pergunta):
    TIPO = 3

    class Meta:
        verbose_name = "Pergunta Arquivo"
        verbose_name_plural = "Perguntas Arquivo"

class PerguntaImagem(Pergunta):
    TIPO = 4

    class Meta:
        verbose_name = "Pergunta Imagem"
        verbose_name_plural = "Perguntas Imagem"

class PerguntaCoordenada(Pergunta):
    TIPO = 5

    class Meta:
        verbose_name = "Pergunta Coordenada"
        verbose_name_plural = "Perguntas Coordenada"

class PerguntaNumero(Pergunta):
    TIPO = 6
    unidade_medida = models.ForeignKey(UnidadeMedida, on_delete = models.CASCADE)
    maior_que = models.FloatField(blank= True, null = True)
    menor_que = models.FloatField(blank= True, null = True)

    class Meta:
        verbose_name = "Pergunta Numero"
        verbose_name_plural = "Perguntas Numero"


class PerguntaDoQuestionario(UUIDModelMixin, TimedModelMixin):
    questionario = models.ForeignKey(Questionario, on_delete = models.CASCADE)
    pergunta = models.ForeignKey(Pergunta, on_delete = models.CASCADE)
    ordem = models.PositiveSmallIntegerField()

    objects = models.Manager()

    class Meta:
        unique_together = ("questionario", "pergunta")
        ordering = ("questionario","ordem","pergunta")
        verbose_name = "Pergunta do Questionario"
        verbose_name_plural = "Perguntas dos Questionarios"


class PossivelEscolha(UUIDModelMixin, TimedModelMixin):
    pergunta = models.ForeignKey(Pergunta, on_delete = models.CASCADE, related_name="possiveis_escolhas")
    texto = models.TextField()

    objects = models.Manager()

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
    localizacao = models.ForeignKey(Localizacao, on_delete = models.CASCADE, null = True, blank = True)

    objects = models.Manager()

    class Meta:
        unique_together = ("resposta_questionario", "pergunta")
        verbose_name = "Resposta da Pergunta"
        verbose_name_plural = "Respostas das Perguntas"

class PossivelEscolhaResposta(UUIDModelMixin, TimedModelMixin):
    resposta_pergunta = models.ForeignKey(RespostaPergunta, on_delete = models.CASCADE, related_name="escolhas")
    possivel_escolha = models.ForeignKey(PossivelEscolha, on_delete = models.CASCADE)

    objects = models.Manager()

    class Meta:
        verbose_name = "Possivel Escolha Resposta"
        verbose_name_plural = "Possiveis Escolhas Resposta"
        unique_together = ("resposta_pergunta", "possivel_escolha")

class CoordenadaResposta(UUIDModelMixin, TimedModelMixin):
    resposta_pergunta = models.ForeignKey(RespostaPergunta, on_delete = models.CASCADE, related_name="coordenadas")
    coordenada = models.ForeignKey(Localizacao, on_delete = models.CASCADE, null = True)

    objects = models.Manager()

    class Meta:
        verbose_name = "Coordenada Resposta"
        verbose_name_plural = "Coordenadas Resposta"
        unique_together = ("resposta_pergunta", "coordenada")

class TextoResposta(UUIDModelMixin, TimedModelMixin):
    resposta_pergunta = models.ForeignKey(RespostaPergunta, on_delete = models.CASCADE, related_name="textos")
    texto = models.TextField()

    objects = models.Manager()

    class Meta:
        verbose_name = "Texto Resposta"
        verbose_name_plural = "Textos Resposta"

class NumeroResposta(UUIDModelMixin, TimedModelMixin):
    resposta_pergunta = models.ForeignKey(RespostaPergunta, on_delete = models.CASCADE, related_name="numeros")
    unidade_medida = models.ForeignKey(UnidadeMedida, on_delete = models.CASCADE)
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
    return "questionarios/arquivos/{}/{}/{}/{}".format( hoje.year, hoje.month, hoje.day, nome_arquivo)

class ArquivoResposta(UUIDModelMixin, TimedModelMixin):
    resposta_pergunta = models.ForeignKey(RespostaPergunta, on_delete = models.CASCADE, related_name="arquivos")
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
    return "questionarios/imagens/{}/{}/{}/{}".format( hoje.year, hoje.month, hoje.day, nome_arquivo)

class ImagemResposta(UUIDModelMixin, TimedModelMixin):
    resposta_pergunta = models.ForeignKey(RespostaPergunta, on_delete = models.CASCADE, related_name="imagens")
    imagem = models.ImageField(upload_to=caminho_para_imagens)

    objects = models.Manager()

    class Meta:
        verbose_name = "Imagem Resposta"
        verbose_name_plural = "Imagens Resposta"
