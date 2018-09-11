from django.contrib import admin

from .models import (
    Relatorio,
    Bloco,
    Editor,
    Figura,
)

class RelatorioAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "titulo", "criado_em")

admin.site.register(Relatorio, RelatorioAdmin)

class BlocoAdmin(admin.ModelAdmin):
    list_display = ("id", "relatorio", "titulo", "nivel", "editor","criado_em")
    readonly_fields = ("nivel",)

admin.site.register(Bloco, BlocoAdmin)

class EditorAdmin(admin.ModelAdmin):
    list_display = ("id", "bloco", "editor", "criado_em")

admin.site.register(Editor, EditorAdmin)

admin.site.register(Figura)
