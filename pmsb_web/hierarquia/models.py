from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
""" Model Mixins """

class UserOwnedModelMixin(models.Model):
    owner = models.ForeignKey(User, on_delete = models.CASCADE)
    class Meta:
        abstract = True

class UUIDModelMixin(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    class Meta:
        abstract = True

""" Final Model Mixins """


""" Hierarquia Horizontal  """

class Departamento(UUIDModelMixin):
    nome         = models.CharField(max_length = 255)
    departamento_pertencente = models.ForeignKey('self', on_delete = models.CASCADE, blank=True,null = True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "Departamento";verbose_name_plural = "Departamentos"
    
    def __str__(self):
        return "{0}".format(self.nome)

class Pessoa(UUIDModelMixin, UserOwnedModelMixin):
    nome             = models.CharField(max_length = 255)
    isCoordenador    = models.BooleanField(null = False)
    departamento_pessoa = models.ForeignKey(Departamento, on_delete = models.CASCADE)

    class Meta:
        ordering = ("isCoordenador", "nome")
        verbose_name = "Pessoa"
        verbose_name_plural = "Pessoas"
    
