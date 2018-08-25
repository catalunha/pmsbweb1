from django import forms

from .models import (
    Relatorio,
    Bloco,
)

class RelatorioForm(forms.ModelForm):
    class Meta:
        model = Relatorio
        fields = ("titulo",)

class BlocoForm(forms.ModelForm):
    class Meta:
        model = Bloco
        fields = "__all__"