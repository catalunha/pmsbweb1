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
        relatorio_pk = kwargs.pop("relatorio_pk")
        super(BlocoForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Bloco
        fields = ("titulo", "descricao")

class BlocoSuperiorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super (BlocoSuperiorForm,self ).__init__(*args,**kwargs) 
        bloco = kwargs.pop("instance")
        filhos = bloco.get_arvore_genealogica()
        queryset = Bloco.objects.filter(fake_deletado=False, relatorio=bloco.relatorio).exclude(pk__in = [filho.pk for filho in filhos])
        self.fields["nivel_superior"].queryset = queryset
    
    class Meta:
        model = Bloco
        fields = ("nivel_superior",)

class BlocoChangeForm(forms.ModelForm):
    class Meta:
        model = Bloco
        fields = ("titulo", "descricao")

class BlocoTextoForm(forms.ModelForm):
    class Meta:
        model = Bloco
        fields = ("texto",)


class BlocoOrdemAjaxForm(forms.ModelForm):
    class Meta:
        model = Bloco
        fields = ("ordem",)

class EditorForm(forms.ModelForm):
    class Meta:
        model = Editor
        fields = ("editor", )

class FiguraForm(forms.ModelForm):
    class Meta:
        model = Figura
        fields = ("imagem", "legenda", "descricao")
        
