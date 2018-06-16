# encoding: utf-8
# django imports
from django.shortcuts import render, redirect 
from django.views.generic.base import View
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


# project imports
from .forms import RegisterPerfilForm, RegisterUserForm
from .models import User, Perfil




class ResgisterUser(View):
    '''
        Class-Based Veiw pra registrar um usuário no sistema
    '''
    template_name = 'conta/registrar.html'
    # adiciono os 2 formularios (abstract_user, perfil)
    # pra criar de uma so vez o user e o seu perfil
    def get(self, request):
        formulario_Abstract_User = RegisterUserForm()
        formulario_Perfil = RegisterPerfilForm()
        return render(request, self.template_name, {'formulario_User': formulario_Abstract_User, 'formulario_Perfill': formulario_Perfil})
    
    # salvar no banco o deferido post do formulario
    def post(self, request):
        # pego o formulário se for metodo = post
        formUser = RegisterUserForm(request.POST, request.FILES)
        # verifico se o formulario esta correto
        if formUser.is_valid():
            # pego os dados do formulario
            dados_formUser = formUser.data
            # salvo o Abstract User
            formUser.save()
            
            # pego a referencia desse novo usuario
            new_user = User.objects.get(username=dados_formUser['username'])
            # adiciono mais dados do AbstractUser com o Perfil.
            new_user_perfil = Perfil(usuario=new_user, sexo=dados_formUser['sexo'],
                                    telefone_celular=dados_formUser['telefone_celular'], telefone_fixo=dados_formUser['telefone_fixo'],
                                    endereco=dados_formUser['endereco'],cep=dados_formUser['cep'],cidade=dados_formUser['cidade'],
                                    uf=dados_formUser['uf'] )
            # salvo o Perfil linkando ao seu respectivo AbstractUser
            new_user_perfil.save()
            # autentico o novo usuario
            user = authenticate(request, username=dados_formUser['username'], password=dados_formUser['password1'])
            if user is not None:
                #login sucesso
                # dashboard
                login(request, user)
                return redirect('dashboard')
            return redirect('dashboard')
        # retorno o formulário vazia se o formulario incorreto
        return self.get(request)

class Dashboard():
    @login_required(login_url='login')
    def painel(request):
        # passo o usuario
        # futuramente passo a estrutura da árvore
        if request.user.is_authenticated:
            user = Perfil.objects.get(usuario_id=request.user.id)
        
        return render(request, 'dashboard/index.html', {'perfil_logado': user})
    
    # outras funcionalidades

def login_view(request):
    '''
    Function-Based View pra logar o usuario no sistemas
    '''
    if request.method == 'POST':
        # antetico o usuario
        #user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        try:
            user = authenticate(username=request.POST['username'],password=request.POST['password'])
            if user is not None:
                #testo se e superuser redireciono admin/
                if user.is_staff:
                    login(request, user)
                    return redirect('admin/')
                else:
                    login(request, user)
                    return redirect('dashboard')
            else:
                # erro no login (senha/usuario errado)
                return render(request, "conta/login.html", {'erro': True})
        except:
            # erro ao logar (usuario n existe)
            return render(request, "conta/login.html", {'erro': True})
    # se o metodo for get só retorno um formulario vazio
    return render(request, "conta/login.html")

def logout_view(request):
    '''
    Function-Based View pra deslogar o usuario do sistemas
    '''
    # deslogo o usuario
    logout(request)
    # redieciono pra página de login
    return redirect('login')