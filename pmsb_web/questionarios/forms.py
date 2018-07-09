from django import forms
from .models import Questionario

class QuestionarioForm(forms.ModelForm):
    class Meta:
        model = Questionario
        fields = ("nome", )