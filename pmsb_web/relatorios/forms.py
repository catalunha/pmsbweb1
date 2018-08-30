from django import forms
from django.shortcuts import get_object_or_404
from .models import (
    Relatorio,
    Bloco,
    Editor,
    Figura,
)

class RelatorioForm(forms.ModelForm):
    class Meta:
        model = Relatorio
        fields = ("titulo", "descricao")

class BlocoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.relatorio = kwargs.pop("relatorio")
        super(BlocoForm, self).__init__(*args, **kwargs)
        self.fields["nivel_superior"].queryset = Bloco.objects.filter(relatorio= self.relatorio)

    class Meta:
        model = Bloco
        fields = ("titulo", "nivel_superior" ,"descricao", "texto")

class BlocoChangeForm(forms.ModelForm):
    class Meta:
        model = Bloco
        fields = ("titulo", "texto", "descricao")

class EditorForm(forms.ModelForm):
    class Meta:
        model = Editor
        fields = ("editor", )

class FiguraForm(forms.ModelForm):
    class Meta:
        model = Figura
        fields = ("imagem", "legenda", "descricao")
        