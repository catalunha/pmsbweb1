import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from model_utils.managers import InheritanceManager
from core.mixins import UUIDModelMixin, UserOwnedModelMixin, TimedModelMixin

class Localizacao(UUIDModelMixin):
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

    @property
    def perguntas_ordenadas(self):
        return PerguntaDoQuestionario.objects.filter(questionario = self).order_by("ordem")

class PerguntaManger(models.Manager):
    def by_questionario(self, questionario, exclude_obj = None):
        queryset = self.get_queryset().filter(questionarios = questionario)
        if exclude_obj is not None:
            queryset = queryset.exclude(pk = exclude_obj.pk)
        return queryset

class Pergunta(UUIDModelMixin, UserOwnedModelMixin, TimedModelMixin):

    TIPO = None

    variavel = models.CharField(max_length = 255)
    texto = models.TextField()
    tipo = models.PositiveSmallIntegerField(editable = False)
    pergunta_requisito = models.ForeignKey("Pergunta", on_delete = models.SET_NULL, null = True, blank = True, related_name="pre_requisito_de")
    possivel_escolha_requisito = models.ForeignKey("PossivelEscolha", on_delete = models.SET_NULL, null = True, blank = True, related_name="pre_requisito_de")
    
    objects = PerguntaManger()
    inherited_objects = InheritanceManager()

    class Meta:
        ordering = ("tipo",)
        verbose_name = "Pergunta"
        verbose_name_plural = "Perguntas"

    def __str__(self):
        return "{}: {}".format(self.variavel, self.texto)
    
    def save(self, *args, **kwargs):
        if not self.tipo:
            self.tipo = self.TIPO
        super(Pergunta, self).save(*args, **kwargs)
    
        #atualiza editado_em nos questionarios com esta pergunta
        for questionario in self.questionarios.all():
            questionario.save()

    @property
    def verbose_name_tipo(self):

        if self.tipo == PerguntaEscolha.TIPO:
            return "Pergunta Escolha"
        elif self.tipo == PerguntaTexto.TIPO:
            return "Pergunta Texto"
        elif self.tipo == PerguntaCoordenada.TIPO:
            return "Pergunta Coordenada"
        elif self.tipo == PerguntaArquivo.TIPO:
            return "Pergunta Arquivo"
        elif self.tipo == PerguntaImagem.TIPO:
            return "Pergunta Imagem"
        elif self.tipo == PerguntaNumero.TIPO:
            return "Pergunta Numero"
    
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
            

class UnidadeMedida(UUIDModelMixin):
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


class PerguntaEscolha(Pergunta):
    TIPO = 0
    multipla = models.BooleanField(default = False)

    class Meta:
        verbose_name = "Pergunta Escolha"
        verbose_name_plural = "Perguntas Escolha"

class PerguntaTexto(Pergunta):
    TIPO = 1

    class Meta:
        verbose_name = "Pergunta Texto"
        verbose_name_plural = "Perguntas Texto"

class PerguntaArquivo(Pergunta):
    TIPO = 2

    class Meta:
        verbose_name = "Pergunta Arquivo"
        verbose_name_plural = "Perguntas Arquivo"

class PerguntaImagem(Pergunta):
    TIPO = 3

    class Meta:
        verbose_name = "Pergunta Imagem"
        verbose_name_plural = "Perguntas Imagem"

class PerguntaCoordenada(Pergunta):
    TIPO = 4

    class Meta:
        verbose_name = "Pergunta Coordenada"
        verbose_name_plural = "Perguntas Coordenada"

class PerguntaNumero(Pergunta):
    TIPO = 5
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
    
    def save(self, *args, **kwargs):
        if self.ordem is None:
            queryset = PerguntaDoQuestionario.objects.filter(questionario = self.questionario)
            ultimo = queryset.last()

            if ultimo is None:
                self.ordem = 1
            else:
                self.ordem = ultimo.ordem + 1
        
        super(PerguntaDoQuestionario, self).save(*args, **kwargs)


class PossivelEscolha(UUIDModelMixin, TimedModelMixin):
    pergunta = models.ForeignKey(PerguntaEscolha, on_delete = models.CASCADE, related_name="possiveis_escolhas")
    texto = models.TextField()

    objects = models.Manager()

    class Meta:
        verbose_name = "Possivel Escolha"
        verbose_name_plural = "Possiveis Escolhas"

    def __str__(self):
        return "{0} -> {1}".format(self.pergunta, self.texto)
    
    @classmethod
    def by_questionario(cls, questionario, exclude_pergunta = None):
        escolhas = PossivelEscolha.objects.filter(pergunta__in = questionario.perguntas.all())
        if exclude_pergunta and isinstance(exclude_pergunta, PerguntaEscolha):
            escolhas = escolhas.exclude( pergunta = exclude_pergunta )
        return escolhas

class RespostaQuestionario(UUIDModelMixin, UserOwnedModelMixin, TimedModelMixin):
    questionario = models.ForeignKey(Questionario, on_delete = models.CASCADE, related_name="respostas")
    objects = models.Manager()

    class Meta:
        verbose_name = "Resposta Questionario"
        verbose_name_plural = "Respostas Questionarios"

    def __str__(self):
        return "Resposta do {0}".format(self.questionario)

class RespostaPergunta(UUIDModelMixin, TimedModelMixin):
    resposta_questionario = models.ForeignKey(RespostaQuestionario, on_delete = models.CASCADE, related_name="perguntas")
    pergunta = models.ForeignKey(Pergunta, on_delete = models.CASCADE)
    localizacao = models.ForeignKey(Localizacao, on_delete = models.CASCADE, null = True, blank = True)

    objects = models.Manager()

    class Meta:
        unique_together = ("resposta_questionario", "pergunta")
        verbose_name = "Resposta da Pergunta"
        verbose_name_plural = "Respostas das Perguntas"
    
    @property
    def tipo(self):
        return self.pergunta.tipo

class PossivelEscolhaResposta(UUIDModelMixin, TimedModelMixin):
    resposta_pergunta = models.ForeignKey(RespostaPergunta, on_delete = models.CASCADE, related_name="escolhas")
    possivel_escolha = models.ForeignKey(PossivelEscolha, on_delete = models.CASCADE)

    objects = models.Manager()

    class Meta:
        verbose_name = "Possivel Escolha Resposta"
        verbose_name_plural = "Possiveis Escolhas Resposta"
        unique_together = ("resposta_pergunta", "possivel_escolha")

class CoordenadaResposta(UUIDModelMixin, TimedModelMixin):
    resposta_pergunta = models.OneToOneField(RespostaPergunta, on_delete = models.CASCADE, related_name="coordenada")
    coordenada = models.ForeignKey(Localizacao, on_delete = models.CASCADE, null = True)

    objects = models.Manager()

    class Meta:
        verbose_name = "Coordenada Resposta"
        verbose_name_plural = "Coordenadas Resposta"
        unique_together = ("resposta_pergunta", "coordenada")

class TextoResposta(UUIDModelMixin, TimedModelMixin):
    resposta_pergunta = models.OneToOneField(RespostaPergunta, on_delete = models.CASCADE, related_name="texto")
    texto = models.TextField()

    objects = models.Manager()

    class Meta:
        verbose_name = "Texto Resposta"
        verbose_name_plural = "Textos Resposta"

class NumeroResposta(UUIDModelMixin, TimedModelMixin):
    resposta_pergunta = models.OneToOneField(RespostaPergunta, on_delete = models.CASCADE, related_name="numero")
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
    resposta_pergunta = models.OneToOneField(RespostaPergunta, on_delete = models.CASCADE, related_name="arquivo")
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
    resposta_pergunta = models.OneToOneField(RespostaPergunta, on_delete = models.CASCADE, related_name="imagem")
    imagem = models.ImageField(upload_to=caminho_para_imagens)

    objects = models.Manager()

    class Meta:
        verbose_name = "Imagem Resposta"
        verbose_name_plural = "Imagens Resposta"
