from django.contrib import admin

from .models import Questionario, Pergunta, PerguntaDoQuestionario, RespostaQuestionario, PossivelEscolha
from .models import RespostaPergunta, ArquivoResposta, ImagemResposta, PossivelEscolhaResposta, TextoResposta, CoordenadaResposta, NumeroResposta
from .models import Localizacao, UnidadeMedida
from .models import PerguntaArquivo, PerguntaCoordenada, PerguntaImagem, PerguntaMultiplaEscolha, PerguntaUnicaEscolha, PerguntaTexto, PerguntaNumero

admin.site.register(Localizacao)
admin.site.register(UnidadeMedida)

#questionario
class RespostaStackedInlineAdmin(admin.StackedInline):
    model = RespostaQuestionario
    extra = 0

class PerguntaDoQuestionarioInlineAdmin(admin.StackedInline):
    model = PerguntaDoQuestionario
    extra = 0

class QuestionarioAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "publicado")
    inlines = (PerguntaDoQuestionarioInlineAdmin, RespostaStackedInlineAdmin)

admin.site.register(Questionario, QuestionarioAdmin)


# pergunta e seus tipos
class PossivelEscolhaStackedInline(admin.StackedInline):
    model = PossivelEscolha
    extra = 0

class PerguntaAdmin(admin.ModelAdmin):
    list_display = ("id", "variavel", "texto", "possivel_escolha_requisito")
    readonly_fields = ("tipo", )

class PerguntaInlinesAdmin(PerguntaAdmin):
    inlines = (PossivelEscolhaStackedInline, )

admin.site.register(Pergunta, PerguntaInlinesAdmin)

class PerguntaUnicaEscolhaAdmin(PerguntaInlinesAdmin):
    pass

admin.site.register(PerguntaUnicaEscolha, PerguntaUnicaEscolhaAdmin)

class PerguntaMultiplaEscolhaAdmin(PerguntaInlinesAdmin):
    pass

admin.site.register(PerguntaMultiplaEscolha, PerguntaMultiplaEscolhaAdmin)

class PerguntaTextoAdmin(PerguntaAdmin):
    pass

admin.site.register(PerguntaTexto, PerguntaTextoAdmin)

class PerguntaArquivoAdmin(PerguntaAdmin):
    pass

admin.site.register(PerguntaArquivo, PerguntaArquivoAdmin)

class PerguntaImagemAdmin(PerguntaAdmin):
    pass

admin.site.register(PerguntaImagem, PerguntaImagemAdmin)

class PerguntaCoordenadaAdmin(PerguntaAdmin):
    pass

admin.site.register(PerguntaCoordenada, PerguntaCoordenadaAdmin)

class PerguntaNumeroAdmin(PerguntaAdmin):
    list_display = PerguntaAdmin.list_display + ("unidade_medida", "maior_que", "menor_que")

admin.site.register(PerguntaNumero, PerguntaNumeroAdmin)

#resposta questionario

class RespostaPerguntaStackedInline(admin.StackedInline):
    model = RespostaPergunta
    extra = 0

class RespostaQuestionarioAdmin(admin.ModelAdmin):
    list_display = ("id", "questionario")
    inlines = (RespostaPerguntaStackedInline, )

admin.site.register(RespostaQuestionario, RespostaQuestionarioAdmin)

#resposta pergunta

class ArquivoRespostaStackedInline(admin.StackedInline):
    model = ArquivoResposta
    extra = 0

class ImagemRespostaStackedInline(admin.StackedInline):
    model = ImagemResposta
    extra = 0

class TextoRespostaStackedInline(admin.StackedInline):
    model = TextoResposta
    extra = 0

class NumeroRespostaStackedInline(admin.StackedInline):
    model = NumeroResposta
    extra = 0

class CoordenadaRespostaStackedInline(admin.StackedInline):
    model = CoordenadaResposta
    extra = 0

class PossivelEscolhaRespostaStackedInline(admin.StackedInline):
    model = PossivelEscolhaResposta
    extra = 0

class RespostaPerguntaAdmin(admin.ModelAdmin):
    list_display = ("id", "resposta_questionario", "pergunta")
    inlines = (
        ArquivoRespostaStackedInline,
        ImagemRespostaStackedInline,
        TextoRespostaStackedInline,
        NumeroRespostaStackedInline,
        CoordenadaRespostaStackedInline,
        PossivelEscolhaRespostaStackedInline,
    )

admin.site.register(RespostaPergunta, RespostaPerguntaAdmin)

class ArquivoRespostaAdmin(admin.ModelAdmin):
    list_display = ("id", "arquivo", "resposta_pergunta", "criado_em")

admin.site.register(ArquivoResposta, ArquivoRespostaAdmin)

admin.site.register(PossivelEscolhaResposta)

admin.site.register(TextoResposta)

admin.site.register(CoordenadaResposta)

