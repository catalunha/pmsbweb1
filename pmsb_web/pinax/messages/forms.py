from django import forms
from django.contrib.auth import get_user_model
from django.forms import ModelForm, FileInput, TextInput, Select, EmailInput, PasswordInput, Textarea, DateInput
from .hooks import hookset
from .models import Message


class UserModelChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return hookset.display_name(obj)


class UserModelMultipleChoiceField(forms.ModelMultipleChoiceField):

    def label_from_instance(self, obj):
        return hookset.display_name(obj)


class NewMessageForm(forms.ModelForm):

    subject = forms.CharField()
    data_de_entrega = forms.DateField()
    to_user = UserModelChoiceField(queryset=get_user_model().objects.none())
    content = forms.CharField(widget=forms.Textarea)
    arquivo = forms.FileField()

    field_order = ['subject', 'data_de_entrega', 'to_user', 'content']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(NewMessageForm, self).__init__(*args, **kwargs)
        self.fields["to_user"].queryset = hookset.get_user_choices(self.user).filter(is_superuser=False).exclude(is_active=False)
        if self.initial.get("to_user") is not None:
            qs = self.fields["to_user"].queryset.filter(pk=self.initial["to_user"])
            self.fields["to_user"].queryset = qs
        self.fields["to_user"].label = "Para " 
        self.fields["subject"].label = "Título da Tarefa "
        self.fields["content"].label =  "Descrição Detalhada "
        self.fields["subject"].widget = TextInput(attrs={'class': 'form-control'})
        self.fields["content"].widget =  Textarea(attrs={'class': 'form-control'})
        self.fields["data_de_entrega"].widget =  DateInput(attrs={'class': 'form-control', 'type':'date', 'required':True})
        self.fields["arquivo"].required = False

    def save(self, commit=True):
        data = self.cleaned_data
        return Message.new_message(
            self.user, [data["to_user"]], data["subject"], data["content"], 
            data["data_de_entrega"],
            data["arquivo"]
        )

    class Meta:
        model = Message
        fields = ["to_user", "subject", "content"]
        


class NewMessageFormMultiple(forms.ModelForm):
    subject = forms.CharField()
    to_user = UserModelMultipleChoiceField(get_user_model().objects.none())
    content = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(NewMessageFormMultiple, self).__init__(*args, **kwargs)
        self.fields["to_user"].queryset = hookset.get_user_choices(self.user).filter(is_superuser=False)
        if self.initial.get("to_user") is not None:
            qs = self.fields["to_user"].queryset.filter(pk__in=self.initial["to_user"])
            self.fields["to_user"].queryset = qs

    def save(self, commit=True):
        data = self.cleaned_data
        return Message.new_message(
            self.user, data["to_user"], data["subject"], data["content"]
        )

    class Meta:
        model = Message
        fields = ["to_user", "subject", "content"]


class MessageReplyForm(forms.ModelForm):
    arquivo = forms.FileField()

    def __init__(self, *args, **kwargs):
        self.thread = kwargs.pop("thread")
        self.user = kwargs.pop("user")
        super(MessageReplyForm, self).__init__(*args, **kwargs)
        
        self.fields["content"].label = ""
        self.fields["content"].widget =  Textarea(attrs={'class': 'form-control', 'placeholder':'Digite detalhadamente o procedimento da tarefa'})
        self.fields["arquivo"].required = False

    def save(self, commit=True):
        return Message.new_reply(
            self.thread, self.user, self.cleaned_data["content"], self.cleaned_data["arquivo"]
        )

    class Meta:
        model = Message
        fields = ["content"]
