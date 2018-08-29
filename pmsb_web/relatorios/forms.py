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
    class Meta:
        model = Bloco
        fields = ("titulo", "descricao", "texto", "nivel_superior")

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
        