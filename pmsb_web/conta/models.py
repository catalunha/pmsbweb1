from django.db import models
from django.contrib.auth.models import AbstractUser

""" Model Mixins """
from questionarios.models import UserOwnedModelMixin
from questionarios.models import UUIDModelMixin
""" Final Model Mixins """

""" Hierarquia Horizontal  """
class Departamento(UUIDModelMixin):
    nome = models.CharField(max_length = 255, unique = True)
    superior = models.ForeignKey('self', on_delete = models.CASCADE, blank=True, null = True)
    descricao = models.TextField(verbose_name="Descrição")

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
    nome = models.CharField(max_length = 255, unique = True)
    descricao = models.TextField(verbose_name="Descrição")

    class Meta:
        ordering = ["nome"]
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"
    
    def __str__(self):
        return "{0}".format(self.nome)

def upload_foto_usuario(instance, filename):
    return "{0}_{1}".format(instance.pk, filename)

class User(AbstractUser):

    SEXO_CHOICE = (
        ("M", "Masculino"),
        ("F", "Feminino"),
        ("ND", "Não-Declara"),
    )
    
    #foto de perfil
    foto = models.ImageField(upload_to=upload_foto_usuario, null = True)

    #n renderizar no formulario
    superior = models.ForeignKey('self', on_delete = models.SET_NULL, blank = True, null = True, related_name="subordinados")

    # referencias com as tabelas
    departamento = models.ForeignKey(Departamento, on_delete = models.SET_NULL, null = True)

    cargo = models.ForeignKey(Cargo, on_delete = models.SET_NULL, null = True)

    # atributos do usuario
    sexo = models.CharField(max_length=2, choices = SEXO_CHOICE, blank = True)
    data_nascimeto = models.DateField(blank=True, null = True, verbose_name="Data de Nascimento")

    #contato
    telefone_celular = models.CharField(max_length=12, blank=True)
    telefone_fixo = models.CharField(max_length=12, blank=True)
    
    #endereço
    cep = models.CharField(max_length=8, blank=True)
    cidade = models.CharField(max_length=25)
    uf = models.CharField(max_length=2)

def SET_SUPERIOR():
    """
    Define novo superior no caso de superior ser deletado do banco de dados
    """
    pass


class UserProfile(UUIDModelMixin):

    usuario = models.OneToOneField(User, on_delete = models.CASCADE, editable = False)
    
    # so anexo
    comprovante_votacao = models.ImageField(upload_to='usuario/comprovante_votacao', blank=True, null = True)
    certidao_nascimento = models.ImageField(upload_to='usuario/certidao_nascimento', blank=True, null = True)
    certidao_casamento = models.ImageField(upload_to='usuario/certidao_casamento', blank=True, null = True)
    carteira_vacinacao = models.ImageField(upload_to='usuario/carteira_vacinacao', blank=True, null = True)
    
    # dado + anexo
    endereco = models.CharField(max_length=50, blank=True, null=True)
    titulo_eleitor = models.CharField(max_length=12, blank=True, null=True)
    cpf = models.CharField(max_length=11)
    
    matricula_uft = models.CharField(max_length=10, blank=True, null=True)
    carteira_motorista = models.ImageField(upload_to='usuario/cnh', blank=True, null = True)
    lattes = models.ImageField(upload_to='usuario/lattes', blank=True, null = True)
    lattes_descricao = models.CharField(max_length=255, blank=True, null=True)


    class Meta:
        ordering = ["usuario"]
        verbose_name = "Perfil do Usuário"
        verbose_name_plural = "Perfis dos Usuários"
    
    def __str__(self):
        return "{0}".format(self.usuario.first_name)

class DocumentoDigitalizado(models.Model):
    """Model definition for Arquivo."""
    arquivo = models.FileField()
    usuario = models.ForeignKey(UserProfile, on_delete = models.CASCADE)
    tipo = models.CharField(max_length=255)

    class Meta:
        """Meta definition for Arquivo."""

        verbose_name = 'Arquivo'
        verbose_name_plural = 'Arquivos'

    def __str__(self):
        """Unicode representation of Arquivo."""
        pass

    def get_absolute_url(self):
        """Return absolute url for Arquivo."""
        return ('')

    # TODO: Define custom methods here

