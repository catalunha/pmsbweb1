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
    PossivelEscolha,
)

class QuestionarioForm(forms.ModelForm):
    class Meta:
        model = Questionario
        fields = ("nome", )

class QuestionarioDeleteForm(forms.Form):
    id = forms.UUIDField()
    object_id = None
    def clean(self):
        super(QuestionarioDeleteForm, self).clean()
        if self.cleaned_data.get("id") != self.object_id:
            print(self.cleaned_data.get("id"), self.object_id)
            self.add_error("id", "ID do objeto não confere.")

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

class PossivelEscolhaForm(forms.ModelForm):
    class Meta:
        model = PossivelEscolha
        fields = ("texto", )