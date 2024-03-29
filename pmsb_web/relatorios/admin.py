from django.contrib import admin

from .models import (
    Relatorio,
    Bloco,
    Figura,
    TemplateLatex,
    TemplateLatexRelatorio,
    Bibtex,
)


class TemplateLatexRelatorioInline(admin.TabularInline):
    model = TemplateLatexRelatorio
    extra = 0


class RelatorioAdmin(admin.ModelAdmin):
    list_display = ("id", "titulo", "fake_deletado", "criado_em", "editado_em", "fake_deletado_em")
    list_filter = ("usuario",)
    search_fields = ("fake_deletado",)
    inlines = (TemplateLatexRelatorioInline,)


admin.site.register(Relatorio, RelatorioAdmin)


class BlocoAdmin(admin.ModelAdmin):
    list_display = ("id", "relatorio", "titulo", "ordem", "nivel", "editor", "criado_em")
    readonly_fields = ("nivel",)


admin.site.register(Bloco, BlocoAdmin)

admin.site.register(Figura)
admin.site.register(TemplateLatex)
admin.site.register(TemplateLatexRelatorio)
admin.site.register(Bibtex)
