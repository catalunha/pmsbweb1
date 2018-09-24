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
        fields = ("variavel", "texto", "possivel_escolha_requisito")

class PerguntaArquivoForm(BasePerguntaForm):
    class Meta(BasePerguntaForm.Meta):
        model = PerguntaArquivo

class PerguntaCoordenadaForm(BasePerguntaForm):
    class Meta(BasePerguntaForm.Meta):
        model = PerguntaCoordenada

class PerguntaEscolhaForm(BasePerguntaForm):
    class Meta(BasePerguntaForm.Meta):
        model = PerguntaEscolha
        fields = BasePerguntaForm.Meta.fields + ("multipla", )

class PerguntaImagemForm(BasePerguntaForm):
    class Meta(BasePerguntaForm.Meta):
        model = PerguntaImagem

class PerguntaNumeroForm(BasePerguntaForm):
    class Meta(BasePerguntaForm.Meta):
        model = PerguntaNumero
        fields = BasePerguntaForm.Meta.fields + ("maior_que", "menor_que", "unidade_medida" )

class PerguntaTextoForm(BasePerguntaForm):
    class Meta(BasePerguntaForm.Meta):
        model = PerguntaTexto

class PossivelEscolhaForm(forms.ModelForm):
    class Meta:
        model = PossivelEscolha
        fields = ("texto", )
        widgets = {
          'texto': forms.Textarea(attrs={'rows':2, 'cols':15}),
        }

class PerguntaRequisitoHiddenChangeForm(forms.ModelForm):

    class Meta:
        model = Pergunta
        fields = ("pergunta_requisito", )
        widgets = {
            "pergunta_requisito": forms.HiddenInput(),
        }