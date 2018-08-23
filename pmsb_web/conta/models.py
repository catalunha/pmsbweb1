# encoding: utf-8
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext as _
''' Model Mixins '''
from core.mixins import UserOwnedModelMixin, TimedModelMixin, UUIDModelMixin
""" Final Model Mixins """

""" Hierarquia Horizontal """
class Departamento(UUIDModelMixin, TimedModelMixin):
    nome = models.CharField(max_length = 255)
    superior = models.ForeignKey('self', on_delete = models.CASCADE, blank=True, null = True)
    descricao = models.TextField(verbose_name='Descrição')

    class Meta:
        ordering = ['superior__nome', 'nome']
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
    
    def __concat_str__(self):
        if self.superior is None:
            return self.nome
        else:
            return self.superior.__concat_str__() + ' -> ' + self.nome

    def __str__(self):
        return self.__concat_str__()

class Cargo(UUIDModelMixin, TimedModelMixin):
    nome = models.CharField(max_length = 255)
    descricao = models.TextField(verbose_name='Descrição')

    class Meta:
        ordering = ['nome']
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'
    
    def __str__(self):
        return '{0}'.format(self.nome)

def upload_foto_usuario(instance, filename):
    return 'usuario_foto/{0}/{1}'.format(instance.pk, filename)

class User(AbstractUser, UUIDModelMixin, TimedModelMixin):

    #username = cpf
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("Este cpf já foi cadastrado, comunique a equipe."),
        },
    )

    #nome completo
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    
    #foto de perfil
    foto = models.ImageField(upload_to=upload_foto_usuario, null = True)

    #n renderizar no formulario
    superior = models.ForeignKey('self', on_delete = models.SET_NULL, blank = True, null = True, related_name='subordinados')

    # referencias com as tabelas
    departamento = models.ForeignKey(Departamento, on_delete = models.SET_NULL, blank=True,null = True)

    # cargo
    cargo = models.ForeignKey(Cargo, on_delete = models.SET_NULL, blank=True,null = True)

    # contato
    telefone_celular = models.CharField(max_length=12, blank=True, null=True)

    class Meta:
        unique_together = ('email',)
        ordering = ['first_name',]

    def __str__(self):
        return '{0}: {1}'.format(self.departamento, self.first_name)

class Atributo(UUIDModelMixin, TimedModelMixin):
    nome = models.CharField(max_length = 255)
    descricao = models.TextField(verbose_name='Descrição')
    valor = models.BooleanField(default = True)
    documento = models.BooleanField(default = False)

    def __str__(self):
        return self.nome
    
    def get_absolute_url(self):
        return reverse("conta:perfil_create", args=[self.pk])

class ValorAtributo(UUIDModelMixin, UserOwnedModelMixin, TimedModelMixin):
    tipo = models.ForeignKey(Atributo, on_delete = models.CASCADE)
    valor = models.CharField(max_length = 255)
    
    class Meta:
        unique_together = ('tipo', 'usuario')
        verbose_name = 'Valor do Atributo'
        verbose_name_plural = 'Valores dos Atributos'

    def __str__(self):
        return '{}-{}'.format(self.tipo, self.valor)

def documento_atributo(instance, filename):
    return 'documentos_atributo/{0}/{1}/{2}'.format(instance.usuario_id, instance.tipo.id, filename)

class DocumentoAtributo(UUIDModelMixin, UserOwnedModelMixin, TimedModelMixin):
    """
    Model definition for Arquivo.
    """    
    tipo = models.ForeignKey(Atributo, on_delete = models.CASCADE)
    arquivo = models.FileField(upload_to=documento_atributo)

    class Meta:
        '''
        Meta definition for DocumentoAtributo.
        '''
        unique_together = ('tipo', 'usuario')
        verbose_name = 'Documento de Atributo'
        verbose_name_plural = 'Documentos de Atributo'

