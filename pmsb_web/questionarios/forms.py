from django import forms

from .models import (
    Questionario,
    Pergunta,
    PerguntaArquivo,
    PerguntaCoordenada,
    PerguntaEscolha,
    PerguntaImagem,
    PerguntaNumero,
    PerguntaTexto,
)

class QuestionarioForm(forms.ModelForm):
    class Meta:
        model = Questionario
        fields = ("nome", )


class BasePerguntaForm(forms.ModelForm):
    class Meta:
        model = Pergunta
        fields = "__all__"

class PerguntaArquivoForm(BasePerguntaForm):
    class Meta(BasePerguntaForm.Meta):
        model = PerguntaArquivo

class PerguntaCoordenadaForm(BasePerguntaForm):
    class Meta(BasePerguntaForm.Meta):
        model = PerguntaCoordenada

class PerguntaEscolhaForm(BasePerguntaForm):
    class Meta(BasePerguntaForm.Meta):
        model = PerguntaEscolha

class PerguntaImagemForm(BasePerguntaForm):
    class Meta(BasePerguntaForm.Meta):
        model = PerguntaImagem

class PerguntaNumeroForm(BasePerguntaForm):
    class Meta(BasePerguntaForm.Meta):
        model = PerguntaNumero

class PerguntaTextoForm(BasePerguntaForm):
    class Meta(BasePerguntaForm.Meta):
        model = PerguntaTexto