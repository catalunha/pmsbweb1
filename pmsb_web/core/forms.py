from django import forms
from .mixins import FakeDeleteModelMixin

class FakeDeleteForm(forms.ModelForm):
    id = forms.UUIDField()
    object_id = None

    class Meta:
        model = FakeDeleteModelMixin
        fields = ("id", )

    def clean(self):
        super().clean()
        if self.cleaned_data.get("id") != self.object_id:
            self.add_error("id", "ID do objeto não confere.")