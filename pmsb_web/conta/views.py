# encoding: utf-8
# django imports
from django.shortcuts import render, redirect 
from django.views.generic.base import View
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.forms import UserChangeForm

# project imports
from .forms import RegisterUserForm, AtualizarUserForm
from .models import User

def login_view(request):
    '''
    Function-Based View pra logar o usuario no sistemas
    '''
    if request.user.is_authenticated:
        return redirect('dashboard')
    elif request.method == 'POST':
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



class ResgisterUser(View):
    '''
        Class-Based Veiw pra registrar um usuário no sistema
    '''
    template_name = 'conta/registrar.html'
    # adiciono os 2 formularios (abstract_user, perfil)
    # pra criar de uma so vez o user e o seu perfil
    def get(self, request):
        formulario_Abstract_User = RegisterUserForm()
        #formulario_Perfil = RegisterPerfilForm()
        return render(request, self.template_name, {'formulario_User': formulario_Abstract_User })
    
    # salvar no banco o deferido post do formulario
    def post(self, request):
        # pego o formulário se for metodo = post
        formUser = RegisterUserForm(request.POST, request.FILES)
        # verifico se o formulario esta correto
        if formUser.is_valid():
            formUser = RegisterUserForm(request.POST, request.FILES)
            # pego os dados do formulario
            dados_formUser = formUser.data
            # salvo o Abstract User
            formUser.save()
            # autentico o novo usuario
            user = authenticate(request, username=dados_formUser['username'], password=dados_formUser['password1'])
            if user is not None:
                #login sucesso
                # dashboard
                login(request, user)
                return redirect('dashboard')
            return redirect('dashboard')
        else:
            # retorno o formulário vazia se o formulario incorreto
            formulario_Abstract_User = RegisterUserForm()
            return render(request, self.template_name, {'formulario_User': formulario_Abstract_User, 'Erro': True })


@login_required(login_url='login')
def edit_user(request):
    '''
    Function-Based View pra editar campos do usuario
    '''
    if request.method == 'POST':
        form = AtualizarUserForm(request.POST, request.FILES, instance=request.user)
        #print('FORMULARIO POST',form.data)
        if form.is_valid():
            form.save()
            time = timezone.now()
            args = {'form': form, 'time':time}
            return render(request, 'conta/atualizar.html', args)
    else:
        form = AtualizarUserForm(instance=request.user)
        #print('FORMULARIO GET',form.data)
        time = timezone.now()
        args = {'form': form, 'time':time}
        return render(request, 'conta/atualizar.html', args)

class Dashboard(View):
    
    @login_required(login_url='login')
    def painel(request):
        # passo o usuario e seus dados
        # futuramente passo a estrutura da árvore
        if request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
            time = timezone.now()
        return render(request, 'dashboard/index.html', {'perfil_logado': user, 'time':time})
    
    
    @login_required(login_url='login')
    def user_profile(request):
        '''
        Function-Based View para listar os atributos do usuario
        '''
        time = timezone.now()
        args = {'user': request.user, 'time': time}
        return render(request, 'conta/listardados.html', args)
        # outras funcionalidades
