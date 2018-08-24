import uuid
from django.db import models
from django.conf import settings
from django.utils.timezone import now

class TimedModelMixin(models.Model):
    criado_em = models.DateTimeField(auto_now_add=True)
    editado_em = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class UserOwnedModelMixin(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    class Meta:
        abstract = True
        ordering = ["usuario"]

class UUIDModelMixin(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    class Meta:
        abstract = True

class FakeDeleteModelMixin(models.Model):
    """
    Mixin para 'deletar' objetos sem removelos do banco de dados
    """    
    fake_deletado = models.BooleanField(default = False)
    fake_deletado_em = models.DateTimeField(null = True, blank = True)

    class Meta:
        abstract = True
    

    def fake_delete(self):
        """
        """
        self.fake_deletado = False
        self.fake_deletado_em = now()
        self.save()
