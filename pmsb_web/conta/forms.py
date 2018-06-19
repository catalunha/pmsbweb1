# django imports
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm, FileInput, TextInput, Select, EmailInput, PasswordInput
from django.contrib.auth.admin import UserAdmin

# imports do projeto
from .models import User

'''
    Forms de Create AbstractUser->Perfil
'''
class RegisterUserForm(UserCreationForm):
    field_order = ['username','email',
                    'password1',
                    'password2',
                    'first_name',
                    'last_name',
                    'cpf',
                    'foto',
                    'data_nascimento',
                    'departamento',
                    'cargo']
    
    # rescrevendo o construtor para adequar os fields do formulario
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # removendo helptext do username
        self.fields['username'].help_text = None       
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        # append * pra mostrar que o campo é obrigatório
        self.fields['username'].label += ' * '       
        self.fields['cpf'].label += ' * '
        self.fields['email'].label += ' * '
        self.fields['foto'].label += ' * '
        self.fields['first_name'].label = 'Nome * '       
        self.fields['last_name'].label = 'Sobrenome * '
        # monkey-patch no label password
        self.fields['password1'].widget = PasswordInput(attrs={'class': 'form-control', 'type':'password'})
        self.fields['password2'].widget = PasswordInput(attrs={'class': 'form-control', 'type':'password'})
    
    class Meta(UserCreationForm.Meta):
        model = User
        exclude = ['id','is_superuser','groups','user_permissions','is_staff','last_login','is_active','date_joined','password']
        fields = '__all__'
        widgets = {
            'email': EmailInput(attrs={'class': 'form-control'}),
            'username': TextInput(attrs={'class': 'form-control'}),
            'password1': PasswordInput(attrs={'class': 'form-control', 'type':'password'}), 
            'password2': PasswordInput(attrs={'class': 'form-control', 'type':'password'}), 
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'cpf': TextInput(attrs={'class': 'form-control', 'type':'number'}),
            'superior': Select(attrs={'class': 'form-control'}),
            'departamento': Select(attrs={'class': 'form-control'}),
            'cargo': Select(attrs={'class': 'form-control'}),
            'foto': FileInput(attrs={'class': 'form-control'}),
        }

'''
    Forms de Update AbstractUser->Perfil
'''
class AtualizarUserForm(ModelForm):
    field_order = [ 'first_name',
                    'last_name',
                    'email',
                    'cpf',
                    'foto',
                    'departamento',
                    'cargo']
     # rescrevendo o construtor para adequar os fields do formulario
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # removendo helptext do username
        # self.fields['username'].help_text = None       
        # self.fields['password1'].help_text = None
        # self.fields['password2'].help_text = None
        # append * pra mostrar que o campo é obrigatório
        # self.fields['username'].label += ' * '       
        self.fields['cpf'].label += ' * '
        self.fields['email'].label += ' * '
        self.fields['foto'].label += ' * '
        self.fields['first_name'].label = 'Nome * '       
        self.fields['last_name'].label = 'Sobrenome * '
        # monkey-patch no label password
        # self.fields['password1'].widget = PasswordInput(attrs={'class': 'form-control', 'type':'password'})
        # self.fields['password2'].widget = PasswordInput(attrs={'class': 'form-control', 'type':'password'})

    class Meta:
        model = User
        exclude = ['username','id','password1','password2','password','is_superuser','groups','user_permissions','is_staff','last_login','is_active','date_joined']
        fields = '__all__'
        widgets = {
            'email': EmailInput(attrs={'class': 'form-control'}),
            'username': TextInput(attrs={'class': 'form-control'}),
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'cpf': TextInput(attrs={'class': 'form-control', 'type':'number'}),
            'superior': Select(attrs={'class': 'form-control'}),
            'departamento': Select(attrs={'class': 'form-control'}),
            'cargo': Select(attrs={'class': 'form-control'}),
            'foto': FileInput(attrs={'class': 'form-control'}),
        }
