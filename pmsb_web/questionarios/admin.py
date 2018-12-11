from django.contrib import admin

from .models import (
    Localizacao,
    UnidadeMedida,
)

#perguntas 
from .models import (
    Questionario,
    Pergunta,
    PerguntaEscolha,
    PossivelEscolha,
    PerguntaArquivo,
    PerguntaCoordenada,
    PerguntaImagem,
    PerguntaTexto,
    PerguntaNumero,
    PerguntaDoQuestionario,
    PerguntaRequisito,
    EscolhaRequisito,
)

#respostas 
from .models import (
    RespostaQuestionario,
    RespostaPergunta,
    PossivelEscolhaResposta,
    CoordenadaResposta,
    TextoResposta,
    NumeroResposta,
    ArquivoResposta,
    ImagemResposta,
)

class LocalizacaoAdmin(admin.ModelAdmin):
    list_display = ("id", "latitude", "longitude", "altitude")

admin.site.register(Localizacao, LocalizacaoAdmin)


class UnidadeMedidaAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "sigla")

admin.site.register(UnidadeMedida)

#questionario
class RespostaStackedInlineAdmin(admin.StackedInline):
    model = RespostaQuestionario
    extra = 0

class PerguntaDoQuestionarioInlineAdmin(admin.StackedInline):
    model = PerguntaDoQuestionario
    extra = 0

class QuestionarioAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "publicado", "fake_deletado", "criado_em", "editado_em")
    list_filter = ("publicado", "usuario")
    search_fields = ("nome", )
    inlines = (PerguntaDoQuestionarioInlineAdmin, RespostaStackedInlineAdmin)

admin.site.register(Questionario, QuestionarioAdmin)


# pergunta e seus tipos
class PossivelEscolhaStackedInline(admin.StackedInline):
    readonly_fields = ("id", "pergunta")
    model = PossivelEscolha
    extra = 0

class PerguntaRequisitoStackedInline(admin.StackedInline):
    model = PerguntaRequisito
    extra = 0

class EscolhaRequisitoStackedInline(admin.StackedInline):
    model = EscolhaRequisito
    extra = 0

class PerguntaAdmin(admin.ModelAdmin):
    list_display = ("id", "variavel", "texto", "possivel_escolha_requisito")
    readonly_fields = ("tipo", )
    list_filter = ("usuario", )
    search_fields = ("variavel", "texto")
    readonly_fields = ("criado_em", "editado_em")
    inlines = (PerguntaRequisitoStackedInline, EscolhaRequisitoStackedInline, )

class PerguntaEscolhaAdmin(admin.ModelAdmin):
    fields = ("id", "usuario", "variavel", "texto", "possivel_escolha_requisito", "tipo", "multipla","criado_em", "editado_em")
    list_display = ("id", "variavel", "texto", "possivel_escolha_requisito")
    readonly_fields = ("tipo", "id", "criado_em", "editado_em")
    inlines = (PerguntaRequisitoStackedInline, EscolhaRequisitoStackedInline, PossivelEscolhaStackedInline, )

admin.site.register(PerguntaEscolha, PerguntaEscolhaAdmin)

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
    list_filter = ("questionario", )
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
    list_display = ("id", "resposta_questionario", "pergunta", "tipo")
    list_filter = ("resposta_questionario", "pergunta")
    inlines = []
    
    def get_inline_instances(self, request, obj=None):
        inline_instances = []
        if obj is None:
            pass
        elif obj.tipo == PerguntaEscolha.TIPO:
            inline_instances = [PossivelEscolhaRespostaStackedInline]
        elif obj.tipo == PerguntaArquivo.TIPO:
            inline_instances = [ArquivoRespostaStackedInline]
        elif obj.tipo == PerguntaCoordenada.TIPO:
            inline_instances = [CoordenadaRespostaStackedInline]
        elif obj.tipo == PerguntaImagem.TIPO:
            inline_instances = [ImagemRespostaStackedInline]
        elif obj.tipo == PerguntaTexto.TIPO:
            inline_instances = [TextoRespostaStackedInline]
        elif obj.tipo == PerguntaNumero.TIPO:
            inline_instances = [NumeroRespostaStackedInline]
        
        self.inlines = inline_instances
        return super(RespostaPerguntaAdmin, self).get_inline_instances(request, obj)
    

admin.site.register(RespostaPergunta, RespostaPerguntaAdmin)

class PossivelEscolhaRespostaAdmin(admin.ModelAdmin):
    list_display = ("id", "possivel_escolha", "resposta_pergunta", "criado_em")
    list_filter = ("resposta_pergunta", )

admin.site.register(PossivelEscolhaResposta, PossivelEscolhaRespostaAdmin)


class BaseRespostaAdmin(admin.ModelAdmin):
    list_filter = ("resposta_pergunta__resposta_questionario__questionario", "resposta_pergunta")


class CoordenadaRespostaAdmin(BaseRespostaAdmin):
    list_display = ("id", "coordenada", "resposta_pergunta", "criado_em")
    

admin.site.register(CoordenadaResposta, CoordenadaRespostaAdmin)

class TextoRespostaAdmin(BaseRespostaAdmin):
    list_display = ("id", "texto", "resposta_pergunta", "criado_em")

admin.site.register(TextoResposta, TextoRespostaAdmin)

class NumeroRespostaAdmin(BaseRespostaAdmin):
    list_display = ("id", "numero", "resposta_pergunta", "criado_em")

admin.site.register(NumeroResposta, NumeroRespostaAdmin)


class ArquivoRespostaAdmin(BaseRespostaAdmin):
    list_display = ("id", "arquivo", "resposta_pergunta", "criado_em")

admin.site.register(ArquivoResposta, ArquivoRespostaAdmin)

class ImagemRespostaAdmin(BaseRespostaAdmin):
    list_display = ("id", "imagem", "resposta_pergunta", "criado_em")

admin.site.register(ImagemResposta, ImagemRespostaAdmin)


class PerguntaRequisitoAdmin(admin.ModelAdmin):
    list_display = ("id", "pergunta", "pergunta_requisito", "fake_deletado")
admin.site.register(PerguntaRequisito, PerguntaRequisitoAdmin)

class EscolhaRequisitoAdmin(admin.ModelAdmin):
    list_display = ("id", "pergunta", "questionario", "escolha_requisito", "fake_deletado")
admin.site.register(EscolhaRequisito, EscolhaRequisitoAdmin)
