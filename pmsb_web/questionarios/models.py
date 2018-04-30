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
    owner = models.ForeignKey(User, on_delete = models.CASCADE)
    class Meta:
        abstract = True

class UUIDModelMixin(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    class Meta:
        abstract = True
""" Final Model Mixins """

class Questionario(UUIDModelMixin, UserOwnedModelMixin, TimedModelMixin):
    nome = models.CharField(max_length = 255)
    publicado = models.BooleanField()

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
    ("coordenada", "Coordenada"),
)

class Pergunta(UUIDModelMixin, TimedModelMixin):
    questionario = models.ForeignKey(Questionario, on_delete = models.CASCADE)
    variavel = models.CharField(max_length = 255)
    texto = models.TextField()
    tipo = models.CharField(max_length = 20, choices = TIPO_PERGUNTA_CHOICE)
    possivel_escolha_requisito = models.ForeignKey("PossivelEscolha", on_delete = models.SET_NULL, null = True, blank = True, related_name="pre_requisito_de")
    ordem = models.SmallIntegerField()

    class Meta:
        ordering = ("questionario", "ordem", "tipo")
        verbose_name = "Pergunta"
        verbose_name_plural = "Perguntas"
        unique_together = ("questionario", "variavel")

    def __str__(self):
        return "{0}: {1}".format(self.questionario, self.texto)

class PossivelEscolha(UUIDModelMixin, TimedModelMixin):
    pergunta = models.ForeignKey(Pergunta, on_delete = models.CASCADE, related_name="possiveis_escolhas")
    texto = models.TextField()

    class Meta:
        verbose_name = "Possivel Escolha"
        verbose_name_plural = "Possiveis Escolhas"

    def __str__(self):
        return "{0} -> {1}".format(self.pergunta, self.texto)

class RespostaQuestionario(UUIDModelMixin, UserOwnedModelMixin, TimedModelMixin):
    questionario = models.ForeignKey(Questionario, on_delete = models.CASCADE)
    numero = models.IntegerField(editable=False)

    objects = models.Manager()

    class Meta:
        unique_together = ("questionario", "numero")
        ordering = ("questionario","numero")

        verbose_name = "Resposta Questionario"
        verbose_name_plural = "Respostas Questionarios"

    def __str__(self):
        return "Resposta do {0} numero {1}".format(self.questionario, self.numero)
    
    def save(self, *args, **kwargs):

        if self.numero is None:            
            
            try:
                resposta = RespostaQuestionario.objects.filter(questionario = self.questionario).order_by("-numero")[0]
                self.numero = resposta.numero + 1
            except IndexError:
                self.numero = 1
        
        super(RespostaQuestionario, self).save(*args, **kwargs)

class RespostaPergunta(UUIDModelMixin, TimedModelMixin):
    resposta_questionario = models.ForeignKey(RespostaQuestionario, on_delete = models.CASCADE)
    pergunta = models.ForeignKey(Pergunta, on_delete = models.CASCADE)

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


def arquivo_resposta_upload_to(instance, filename):
    hoje = timezone.now()
    
    try:
        file_uuid = instance.id
    except:
        file_uuid = uuid.uuid4()
    
    nome_arquivo = "{0}_{1}".format(file_uuid, filename)
    return "{0}/{1}/{2}/{3}".format(hoje.year, hoje.month, hoje.day, nome_arquivo)

class ArquivoResposta(UUIDModelMixin, TimedModelMixin):
    resposta_pergunta = models.ForeignKey(RespostaPergunta, on_delete = models.CASCADE, related_name="arquivos")
    arquivo = models.FileField(upload_to=arquivo_resposta_upload_to)

class CoordenadaResposta(UUIDModelMixin, TimedModelMixin):
    resposta_pergunta = models.ForeignKey(RespostaPergunta, on_delete = models.CASCADE, related_name="coordenadas")
    coordenada = models.CharField(max_length = 255)

class TextoResposta(UUIDModelMixin, TimedModelMixin):
    resposta_pergunta = models.ForeignKey(RespostaPergunta, on_delete = models.CASCADE, related_name="textos")
    texto = models.TextField()
    