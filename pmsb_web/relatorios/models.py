from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

from core.mixins import (
    UUIDModelMixin,
    FakeDeleteModelMixin,
    FakeDeleteManagerMixin,
    FakeDeleteQuerysetMixin,
    UserOwnedModelMixin,
    TimedModelMixin,
)

RELATORIOS_MEDIA = "relatorios"

User = get_user_model()

class MaxLevelExceeded(Exception):
    pass

class NivelErrado(Exception):
    pass 

class UpOrdemException(Exception):
    pass

class DownOrdemException(Exception):
    pass

class RelatorioQueryset(FakeDeleteQuerysetMixin, models.QuerySet):
    def by_dono_ou_editor(self, user):
        dono = models.Q(usuario = user)
        editor = models.Q(blocos__editores__editor = user)

        return self.filter(editor | dono).distinct()

class RelatorioManager(FakeDeleteManagerMixin, models.Manager):
    
    def get_queryset(self):
        return RelatorioQueryset(self.model, using=self._db)
    
    def by_dono_ou_editor(self, user):
        return self.get_queryset().by_dono_ou_editor(user)

class Relatorio(UUIDModelMixin, UserOwnedModelMixin, FakeDeleteModelMixin, TimedModelMixin):
    titulo = models.CharField(max_length = 255)
    descricao = models.TextField()
    objetcs = RelatorioManager()

    def __str__(self):
        return self.titulo

class Bloco(UUIDModelMixin, FakeDeleteModelMixin, TimedModelMixin):
    
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
    descricao = models.TextField()
    texto = models.TextField()

    ordem = models.PositiveSmallIntegerField(blank = True)
    nivel_superior = models.ForeignKey("Bloco", null = True, blank = True, on_delete = models.CASCADE, related_name="subblocos")
    nivel = models.PositiveSmallIntegerField(editable = False)

    objects = models.Manager()

    class Meta:
        ordering = ["ordem", "criado_em"]
    
    def __str__(self):
        return "{} - {}".format(self.relatorio, self.titulo)

    def save(self, *args, **kwargs):
        if self.nivel is None:
            if self.nivel_superior is not None:
                self.nivel = self.nivel_superior.nivel_para_filhos()
            else:
                self.nivel = self.PART
        
        if self.nivel > self.NIVEL_MAXIMO:
            raise MaxLevelExceeded("excede nivel maximo de sub-blocos")
        
        if self.ordem is None:
            self.ordem = self.proxima_ordem()
    
        super(Bloco, self).save(*args, **kwargs)
    
    @property
    def usuario(self):
        return self.relatorio.usuario
    
    def nivel_para_filhos(self):
        if self.nivel < self.NIVEL_MAXIMO:
            return self.nivel + 1
        else:
            raise MaxLevelExceeded("excede nivel maximo de sub-blocos")
    
    def proxima_ordem(self):

        queryset = Bloco.objects.filter(relatorio = self.relatorio)

        if self.nivel_superior is None:
            queryset = queryset.filter(nivel_superior = None)
        else:
            queryset = queryset.filter(nivel_superior = self.nivel_superior)

        b = queryset.order_by("-ordem").first()
        if b is None:
            return 0
        else:
            return b.ordem + 1
    
    def muda_nivel_superior(self, novo_superior = None):

        if novo_superior is None:
            novo_nivel = 0
        else:
            novo_nivel = novo_superior.nivel + 1

        if self.delta_nivel_permitido(novo_nivel):
            self.nivel_superior = novo_superior
            self.muda_nivel(novo_nivel)
        else:
            raise MaxLevelExceeded("excede nivel maximo de sub-blocos ao mudar de nivel superior")


    def muda_nivel(self, nivel):
        if self.nivel_superior is None and nivel != 0:
            raise NivelErrado("Não pode ter nivel diferente de 0 quando não tem superior")
        elif self.nivel_superior is not None and nivel != self.nivel_superior.nivel+1:
            raise NivelErrado("Não pode ter nivel diferente ao nivel superior + 1")

        self.nivel = nivel
        self.save()

        for s in self.subblocos.all():
            s.muda_nivel(nivel + 1)
            s.save()
    
    def delta_nivel_permitido(self, novo_nivel):
        p = self.profundidade()
        altura = p - self.nivel
        return novo_nivel + altura <= self.NIVEL_MAXIMO

    def profundidade(self):
        if self.nivel >= self.NIVEL_MAXIMO:
            return self.nivel
        
        maior = self.nivel
        
        for a in self.subblocos.all():
            ap = a.profundidade()
            if ap >= self.NIVEL_MAXIMO:
                return ap
            if ap > maior:
                maior = ap
        
        return maior
        
    def sobe_ordem(self):
        if self.ordem == 0:
            raise UpOrdemException("Bloco nao pode subir")
        irmao = self.subblocos.all()
        irmao.filter(ordem=self.ordem-1)
        self.ordem = self.ordem+1
        irmao.ordem = irmao.ordem-1
        self.save()
        irmao.save()
        
    def desce_ordem(self):
        if self.ordem == self.subblocos.last():
            raise DownOrdemException("Bloco nao pode descer")
        irmao = self.subblocos.filter(ordem=self.ordem+1)
        self.ordem = self.ordem - 1
        irmao.ordem = irmao.ordem + 1
        self.save()
        irmao.save()


class Editor(UUIDModelMixin, UserOwnedModelMixin, FakeDeleteModelMixin, TimedModelMixin):
    bloco = models.ForeignKey(Bloco, on_delete = models.CASCADE, related_name="editores")
    editor = models.ForeignKey(User, on_delete = models.CASCADE, related_name="editor_blocos")

    class Meta:
        unique_together = ("bloco", "editor")

def upload_figura(instance, filename):
    hoje = timezone.now()
    return "{}/figuras/{}/{}/{}/{}-{}".format(RELATORIOS_MEDIA, hoje.year, hoje.month, hoje.day, instance.pk, filename)


class FiguraManager(models.Manager):
    
    def by_dono_ou_editor(self, user):
        dono = Q(usuario = user) #dono imagem
        dono_relatorio = Q(relatorio__usuario = user) # dono relatorio
        editor = Q(relatorio__blocos__editores__editor = user) # editor relatorio

        return self.filter(editor | dono | dono_relatorio)

class Figura(UUIDModelMixin, UserOwnedModelMixin, FakeDeleteModelMixin, TimedModelMixin):
    relatorio = models.ForeignKey(Relatorio, on_delete = models.CASCADE, related_name="figuras")
    imagem = models.ImageField(upload_to = upload_figura, max_length = 255)
    descricao = models.TextField()
    legenda = models.CharField(max_length = 255)

    objetcs = FiguraManager()