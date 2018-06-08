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
    superior = models.ForeignKey('self', on_delete = models.CASCADE, blank=True, null = True)
    teste = models.IntegerField()

    class Meta:
        ordering = ["superior__nome", "nome"]
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"
    
    def __concat_str__(self):
        if self.superior is None:
            return self.nome
        else:
            return self.superior.__concat_str__() + ' -> ' + self.nome

    def __str__(self):
        return self.__concat_str__()


class Cargo(UUIDModelMixin):
    nome = models.CharField(max_length = 255)
    descricao = models.TextField()

    class Meta:
        ordering = ["nome"]
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"

class UserPerfil(UUIDModelMixin):
    usuario = models.OneToOneField(User, on_delete = models.CASCADE)
    
    superior = models.ForeignKey('self', on_delete = models.CASCADE, blank=True, null = True, related_name="subordinados")
    departamento = models.ForeignKey(Departamento, on_delete = models.CASCADE)
    cargo = models.ForeignKey(Cargo, on_delete = models.CASCADE)

    """
    TODO: outros capos do perfil faltando, tem que ver no arquivo pdf do catalunha
    """

    class Meta:
        ordering = ["usuario"]
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"
    
    def __str__(self):
        return "{0}".format(self.usuario.first_name)