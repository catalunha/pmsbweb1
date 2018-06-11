from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

""" Model Mixins """
class TimedModelMixin(models.Model):
    criado_em = models.DateTimeField(auto_now_add=True)
    editado_em = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class UserOwnedModelMixin(models.Model):
    usuario = models.ForeignKey(User, on_delete = models.CASCADE)
    class Meta:
        abstract = True
        ordering = ["usuario"]

class UUIDModelMixin(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    class Meta:
        abstract = True
""" Final Model Mixins """

class Localizacao(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    altitude = models.DecimalField(max_digits=9, decimal_places=6)

"""
    Class Questionario
    documentação
"""
class Questionario(UUIDModelMixin, UserOwnedModelMixin, TimedModelMixin):
    nome = models.CharField(max_length = 255)
    publicado = models.BooleanField()

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

TIPO_PERGUNTA_CHOICE = (
    ("unica-escolha", "Unica Escolha"),
    ("multipla-escolha", "Multipla Escolha"),
    ("texto", "Texto"),
    ("arquivo", "Arquivo"),
    ("imagem", "Imagem"),
    ("coordenada", "Coordenada"),
    ("numero", "Numero"),
)

class Pergunta(UUIDModelMixin, TimedModelMixin):
    variavel = models.CharField(max_length = 255)
    texto = models.TextField()
    tipo = models.CharField(max_length = 20, choices = TIPO_PERGUNTA_CHOICE)
    possivel_escolha_requisito = models.ForeignKey("PossivelEscolha", on_delete = models.SET_NULL, null = True, blank = True, related_name="pre_requisito_de")

    class Meta:
        ordering = ("tipo",)
        verbose_name = "Pergunta"
        verbose_name_plural = "Perguntas"

    def __str__(self):
        return "{0}: {1}".format(self.variavel, self.texto)

class PerguntaDoQuestionario(UUIDModelMixin, TimedModelMixin):
    questionario = models.ForeignKey(Questionario, on_delete = models.CASCADE)
    pergunta = models.ForeignKey(Pergunta, on_delete = models.CASCADE)
    ordem = models.SmallIntegerField()

    class Meta:
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



def upload_to(folder):
    """
        Retorna uma função de upload para arquivos dentro da pasta media/questionarios/{folder}{y}{m}{d}{nome_arquivo}
        nome_arquivo -> uuid_filename
    """
    def upload_to_folder(instance, filename):
        hoje = timezone.now()
        try:
            file_uuid = instance.id
        except:
            file_uuid = uuid.uuid4()
        
        nome_arquivo = "{0}_{1}".format(file_uuid, filename)
        return "questionarios/{0}/{1}/{2}/{3}/{4}".format(folder, hoje.year, hoje.month, hoje.day, nome_arquivo)
    
    return upload_to_folder

class ArquivoResposta(UUIDModelMixin, TimedModelMixin):
    resposta_pergunta = models.ForeignKey(RespostaPergunta, on_delete = models.CASCADE, related_name="arquivos")
    arquivo = models.FileField(upload_to=upload_to("arquivos"))

class ImagemResposta(UUIDModelMixin, TimedModelMixin):
    resposta_pergunta = models.ForeignKey(RespostaPergunta, on_delete = models.CASCADE, related_name="arquivos")
    imagem = models.ImageField(upload_to=upload_to("imagens"))

class CoordenadaResposta(UUIDModelMixin, TimedModelMixin):
    resposta_pergunta = models.ForeignKey(RespostaPergunta, on_delete = models.CASCADE, related_name="coordenadas")
    coordenada = models.CharField(max_length = 255)

class TextoResposta(UUIDModelMixin, TimedModelMixin):
    resposta_pergunta = models.ForeignKey(RespostaPergunta, on_delete = models.CASCADE, related_name="textos")
    texto = models.TextField()

class NumeroResposta(UUIDModelMixin, TimedModelMixin):
    resposta_pergunta = models.ForeignKey(RespostaPergunta, on_delete = models.CASCADE, related_name="numeros")
    numero = models.IntegerField()