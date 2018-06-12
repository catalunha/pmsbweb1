import uuid
from django.db import models
from django.conf import settings

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