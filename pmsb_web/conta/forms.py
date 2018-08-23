# django imports
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import (
    ModelForm,
    FileInput,
    TextInput,
    Select,
    EmailInput,
    PasswordInput
)
from django.contrib.auth.forms import PasswordChangeForm
# imports do projeto
from .models import (
    User,
    Atributo,
    ValorAtributo,
    DocumentoAtributo,
)

'''
    Forms de Create AbstractUser->Perfil
'''
class RegisterUserForm(UserCreationForm):
    field_order = [ 'first_name','last_name','email','username','password1','password2','telefone_celular','foto']
    
    # rescrevendo o construtor para adequar os fields do formulario
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # removendo helptext do username
        self.fields['username'].label = "CPF"
        self.fields['username'].help_text = "Apenas números, Exemplo: 12345678900"       
        self.fields['password2'].help_text = None
        self.fields['first_name'].help_text = "Igual sua identidade."
        self.fields['email'].help_text = "Use preferencialmente gmail"
        self.fields['telefone_celular'].help_text = "Informe DDD+Numero. Use apenas números. Exemplo: 63912345678"
        # mundaca nas labels
        self.fields['first_name'].label = "Nome Completo"
        self.fields['last_name'].label = "Nome usual no projeto"
        self.fields['last_name'].help_text = "Nome curto no qual é conhecido"
        self.fields['password1'].widget = PasswordInput(attrs={'class': 'form-control', 'type':'password'})
        self.fields['password2'].widget = PasswordInput(attrs={'class': 'form-control', 'type':'password'})
        # required tags
        self.fields['telefone_celular'].required=True
        self.fields['first_name'].required=True
        self.fields['last_name'].required=True
        self.fields['email'].required=True
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
        
    class Meta(UserCreationForm.Meta):
        model = User
        exclude = ['id','is_superuser','groups','user_permissions','is_staff','last_login','is_active','date_joined','password','superior','departamento','cargo']
        fields = '__all__'
        widgets = {
            'email': EmailInput(attrs={'class': 'form-control'}),
            'username': TextInput(attrs={'class': 'form-control cpf -mask', 'type':'text', 'id':'cpf'}),
            'password1': PasswordInput(attrs={'class': 'form-control', 'type':'password'}), 
            'password2': PasswordInput(attrs={'class': 'form-control', 'type':'password'}), 
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'superior': Select(attrs={'class': 'form-control'}),
            'departamento': Select(attrs={'class': 'form-control'}),
            'cargo': Select(attrs={'class': 'form-control'}),
            'foto': FileInput(attrs={'class': 'form-control'}),
            'telefone_celular': TextInput(attrs={'class': 'form-control phone_with_ddd -mask', 'type':'text','id':'phone_with_ddd_celular'}),
        }

'''
    Forms de Update AbstractUser->Perfil
'''
class AtualizarUserForm(ModelForm):
    field_order = [ 'first_name','last_name','email','telefone-celular','foto']
    # rescrevendo o construtor para adequar os fields do formulario
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = 'Nome completo'
        self.fields['last_name'].label = 'Nome do projeto'
        self.fields['telefone_celular'].required=True
        self.fields['first_name'].required=True
        self.fields['last_name'].required=True
        self.fields['email'].required=True
        self.fields['foto'].required=False

    class Meta:
        model = User
        exclude = ['username','id','password1','password2','password','is_superuser','groups','user_permissions','is_staff','last_login','is_active','date_joined','superior','cargo']
        fields = ['first_name','last_name','email','telefone_celular','foto']
        widgets = {
            'email': EmailInput(attrs={'class': 'form-control'}),
            'username': TextInput(attrs={'class': 'form-control'}),
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'superior': Select(attrs={'class': 'form-control'}),
            'departamento': Select(attrs={'class': 'form-control'}),
            'cargo': Select(attrs={'class': 'form-control'}),
            'telefone_celular': TextInput(attrs={'class': 'form-control phone_with_ddd -mask', 'type':'text','id':'phone_with_ddd_celular'}),
            'foto': FileInput(attrs={'class': 'form-control'}),
        }

class AtualizarSenhaForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(user, *args, **kwargs)
        self.fields['new_password1'].widget = PasswordInput(attrs={'class': 'form-control', 'type':'password'})
        self.fields['new_password2'].widget = PasswordInput(attrs={'class': 'form-control', 'type':'password'})
        self.fields['old_password'].widget = PasswordInput(attrs={'class': 'form-control', 'type':'password'})

class BaseValorAtributoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        print(args,kwargs)
        super(BaseValorAtributoForm, self).__init__(*args, **kwargs)
        print(self.fields)

    class Meta:
        model = ValorAtributo
        fields = ("valor",)

class BaseDocumentoAtributoForm(ModelForm):
    class Meta:
        model = DocumentoAtributo
        fields = ("arquivo",)