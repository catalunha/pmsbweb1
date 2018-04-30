from django.contrib import admin

from .models import Questionario, Pergunta, RespostaQuestionario, PossivelEscolha
from .models import RespostaPergunta, ArquivoResposta, PossivelEscolhaResposta, TextoResposta, CoordenadaResposta

admin.site.site_header = "PMSB"

admin.site.site_title = "PMSB"


class PerguntaStackedInlineAdmin(admin.StackedInline):
    model = Pergunta
    extra = 0

class RespostaStackedInlineAdmin(admin.StackedInline):
    model = RespostaQuestionario
    extra = 0

class QuestionarioAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "publicado")
    inlines = (PerguntaStackedInlineAdmin, RespostaStackedInlineAdmin)

admin.site.register(Questionario, QuestionarioAdmin)

class PossivelEscolhaStackedInline(admin.StackedInline):
    model = PossivelEscolha
    extra = 0

class PerguntaAdmin(admin.ModelAdmin):
    list_display = ("id", "questionario", "texto", "possivel_escolha_requisito")
    inlines = (PossivelEscolhaStackedInline, )

admin.site.register(Pergunta, PerguntaAdmin)

class RespostaQuestionarioAdmin(admin.ModelAdmin):
    list_display = ("id", "questionario")

admin.site.register(RespostaQuestionario, RespostaQuestionarioAdmin)

admin.site.register(RespostaPergunta)

class ArquivoRespostaAdmin(admin.ModelAdmin):
    list_display = ("id", "arquivo", "resposta_pergunta", "criado_em")

admin.site.register(ArquivoResposta, ArquivoRespostaAdmin)

admin.site.register(PossivelEscolhaResposta)

admin.site.register(TextoResposta)

admin.site.register(CoordenadaResposta)