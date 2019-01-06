from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms

# django project imports
from .forms import RegisterUserForm, AtualizarUserForm
from .models import User, Cargo, Departamento, Atributo, ValorAtributo, DocumentoAtributo
# Register your models here.

ADDITIONAL_USER_FIELDS = (
    ("Informações Adicionais", {'fields': ('foto','departamento','superior','cargo')}),
)


class CustomUserAdmin(UserAdmin):
    model = User
    add_fieldsets = UserAdmin.add_fieldsets + ADDITIONAL_USER_FIELDS
    fieldsets = UserAdmin.fieldsets + ADDITIONAL_USER_FIELDS
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'departamento', 'cargo', 'superior', 'is_active')

admin.site.register(User, CustomUserAdmin)

class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "descricao", "superior", "criado_em", "editado_em")
    list_filter = ('superior', 'criado_em', 'editado_em')
    search_fields = ("nome",)

admin.site.register(Departamento, DepartamentoAdmin)

class CargoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "descricao", "criado_em", "editado_em")
    list_filter = ('criado_em', 'editado_em')
    search_fields = ("nome",)

admin.site.register(Cargo, CargoAdmin)

class AtributoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "descricao", "valor", "documento", "criado_em", "editado_em")
    list_filter = ('criado_em', 'editado_em')
    search_fields = ("nome",)

admin.site.register(Atributo, AtributoAdmin)

class ValorAtributoAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "tipo", "valor", "criado_em", "editado_em")
    list_filter = ('usuario', 'criado_em', 'editado_em')
    search_fields = ("nome",)

admin.site.register(ValorAtributo, ValorAtributoAdmin)

class DocumentoAtributoAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "tipo", "criado_em", "editado_em")
    list_filter = ('usuario', 'criado_em', 'editado_em')
    search_fields = ("nome",)

admin.site.register(DocumentoAtributo, DocumentoAtributoAdmin)