from rest_framework import serializers
from core.mixins import ArquivoBase64SerializerField
from .models import User, Cargo, Departamento, Atributo, DocumentoAtributo, ValorAtributo


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "last_login",
            "is_superuser",
            "last_name",
            "email",
            "is_staff",
            "is_active",
            "date_joined",
            "criado_em",
            "editado_em",
            "username",
            "first_name",
            "foto",
            "telefone_celular",
            "superior",
            "departamento",
            "cargo",
            "groups",
            "user_permissions",
        )


class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = '__all__'


class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = '__all__'


class AtributoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atributo
        fields = '__all__'

class DocumentoAtributoSerializer(serializers.ModelSerializer):
    arquivo = ArquivoBase64SerializerField()
    class Meta:
        model = DocumentoAtributo
        fields = '__all__'


class ValorAtributoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValorAtributo
        fields = '__all__'