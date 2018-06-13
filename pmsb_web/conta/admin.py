from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Cargo, Departamento, Perfil, Atributo, ValorAtributo, DocumentoAtributo
# Register your models here.

class CustomUserAdmin(UserAdmin):
    pass

#admin.site.register(User, CustomUserAdmin)
admin.site.register(User)

class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "descricao", "superior")

admin.site.register(Departamento, DepartamentoAdmin)

class CargoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "descricao")

admin.site.register(Cargo, CargoAdmin)

class PerfilAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "sexo")

admin.site.register(Perfil, PerfilAdmin)

class AtributoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "descricao", "valor", "documento")

admin.site.register(Atributo, AtributoAdmin)

class ValorAtributoAdmin(admin.ModelAdmin):
    list_display = ("usuario", "tipo", "valor")

admin.site.register(ValorAtributo, ValorAtributoAdmin)

class DocumentoAtributoAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "tipo")

admin.site.register(DocumentoAtributo, DocumentoAtributoAdmin)