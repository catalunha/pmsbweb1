from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

from core.mixins import (
    UUIDModelMixin,
    FakeDeleteModelMixin,
    UserOwnedModelMixin,
    TimedModelMixin,
)

RELATORIOS_MEDIA = "relatorios"

User = get_user_model()

class MaxLevelExcided(Exception):
    
    def __init__(self, expression):
        self.expression = expression
        self.message = "excede nivel maximo de sub-blocos"

class Relatorio(UUIDModelMixin, UserOwnedModelMixin, FakeDeleteModelMixin, TimedModelMixin):
    titulo = models.CharField(max_length = 255)

class Bloco(UUIDModelMixin, UserOwnedModelMixin, FakeDeleteModelMixin, TimedModelMixin):
    
    PART = 0
    CHAPTER = 1
    SECTION = 2
    SUBSECTION = 3
    SUBSUBSECTION = 4
    PARAGRAPH = 5
    SUBPARAGRAPH = 6

    NIVEL_MAXIMO = 6

    relatorio = models.ForeignKey(Relatorio, on_delete = models.CASCADE, related_name="blocos")
    titulo = models.CharField(max_length = 255)
    texto = models.TextField()

    nivel_superior = models.ForeignKey("Bloco", null = True, on_delete = models.CASCADE, related_name="subblocos")
    nivel = models.PositiveSmallIntegerField(editable = False)

    def save(self, *args, **kwargs):
        if self.nivel is None:
            if self.nivel_superior is not None:
                self.nivel = self.nivel_superior.nivel_para_filhos()
            else:
                self.nivel = self.PART
        
        if self.nivel > self.NIVEL_MAXIMO:
            raise MaxLevelExcided
    
        super(Bloco, self).save(*args, **kwargs)
    
    def nivel_para_filhos(self):
        if self.nivel < self.NIVEL_MAXIMO:
            return self.nivel + 1
        else:
            raise MaxLevelExcided

class Editor(UUIDModelMixin, UserOwnedModelMixin, FakeDeleteModelMixin, TimedModelMixin):
    bloco = models.ForeignKey(Bloco, on_delete = models.CASCADE, related_name="editores")
    editor = models.ForeignKey(User, on_delete = models.CASCADE, related_name="editor_blocos")

    class Meta:
        unique_together = ("bloco", "editor")

def upload_figura(instance, filename):
    hoje = timezone.now()
    return "{}/figuras/{}/{}/{}/{}-{}".format(RELATORIOS_MEDIA, hoje.year, hoje.month, hoje.day, instance.pk, filename)

class Figura(UUIDModelMixin, UserOwnedModelMixin, FakeDeleteModelMixin, TimedModelMixin):
    relatorio = models.ForeignKey(Relatorio, on_delete = models.CASCADE, related_name="figuras")
    imagem = models.ImageField(upload_to = upload_figura)
    legenda = models.CharField(max_length = 255)