from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms

# django project imports
from .forms import RegisterUserForm, AtualizarUserForm
from .models import User, Cargo, Departamento, Atributo, ValorAtributo, DocumentoAtributo
# Register your models here.

ADDITIONAL_USER_FIELDS = (
    (None, {'fields': ('cpf','email','foto','first_name','last_name','departamento','superior','cargo')}),
)


class CustomUserAdmin(UserAdmin):
    model = User

    add_fieldsets = UserAdmin.add_fieldsets + ADDITIONAL_USER_FIELDS
    fieldsets = UserAdmin.fieldsets + ADDITIONAL_USER_FIELDS

    list_display = ('id', 'username', 'first_name', 'last_name', 'cpf', 'email', 'departamento', 'cargo')

#admin.site.register(User, CustomUserAdmin)
admin.site.register(User)

class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "descricao", "superior")

admin.site.register(Departamento, DepartamentoAdmin)

class CargoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "descricao")

admin.site.register(Cargo, CargoAdmin)

class AtributoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "descricao", "valor", "documento")

admin.site.register(Atributo, AtributoAdmin)

class ValorAtributoAdmin(admin.ModelAdmin):
    list_display = ("usuario", "tipo", "valor")

admin.site.register(ValorAtributo, ValorAtributoAdmin)

class DocumentoAtributoAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "tipo")

admin.site.register(DocumentoAtributo, DocumentoAtributoAdmin)