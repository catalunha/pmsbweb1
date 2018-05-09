from django.db import models
from django.contrib.auth.models import User

""" Model Mixins """
from questionarios.models import UserOwnedModelMixin
from questionarios.models import UUIDModelMixin
""" Final Model Mixins """
import uuid

# Create your models here.
""" Hierarquia Horizontal  """

class Departamento(UUIDModelMixin):
    nome = models.CharField(max_length = 255)
    departamento_pertencente = models.ForeignKey('self', on_delete = models.CASCADE, blank=True,null = True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"
    
    def __concat_str__(self):
        if self.departamento_pertencente is None:
            return self.nome
        else:
            return self.departamento_pertencente.__concat_str__() + ' -> ' + self.nome

    def __str__(self):
        return self.__concat_str__()


class Cargo(UUIDModelMixin):
    nome = models.CharField(max_length = 255)
    descricao = models.TextField()

    class Meta:
        ordering = ["nome"]
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"

class Pessoa(UUIDModelMixin):
    nome = models.CharField(max_length = 255)
    isCoordenador = models.BooleanField(null = False)
    departamento_pessoa = models.ForeignKey(Departamento, on_delete = models.CASCADE)

    class Meta:
        ordering = ["-isCoordenador"]
        verbose_name = "Pessoa"
        verbose_name_plural = "Pessoas"
    
    def __str__(self):
        if self.isCoordenador:
            return "Coordenador {0}".format(self.nome)
        else:
            return "{0}".format(self.nome)

class Hierarquia(UUIDModelMixin):
    usuario = models.OneToOneKey(User, on_delete = models.CASCADE)
    superior = models.ForeignKey('self', on_delete = models.CASCADE, blank=True, null = True)
    departamento = models.ForeignKey(Departamento, on_delete = models.CASCADE)
    cargo = models.ForeignKey(Cargo, on_delete = models.CASCADE)

    class Meta:
        ordering = UserOwnedModelMixin.Meta.ordering
        verbose_name = "Hierarquia"
        verbose_name_plural = "Hierarquia"