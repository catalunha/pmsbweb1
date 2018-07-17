# encoding: utf-8
# django imports
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render, redirect 
from django.views.generic import UpdateView, ListView
from django.views.generic.base import View
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm

# project imports
from .forms import RegisterUserForm, AtualizarUserForm, AtualizarSenhaForm
from .models import User, Atributo

def login_view(request):
    '''
    Function-Based View pra logar o usuario no sistemas
    '''
    if request.user.is_authenticated:
        return redirect('conta:dashboard')
    elif request.method == 'POST':
        try:
            user = authenticate(username=request.POST['username'],password=request.POST['password'])
            if user is not None:
                #testo se e superuser redireciono admin/
                if user.is_staff:
                    login(request, user)
                    return redirect('admin/')
                else:
                    login(request, user)
                    return redirect('conta:dashboard')
            else:
                return render(request, "conta/login.html", {'erro': True})    
        except:
            pass
    # se o metodo for get só retorno um formulario vazio
    return render(request, "conta/login.html")

def logout_view(request):
    '''
    Function-Based View pra deslogar o usuario do sistemas
    '''
    # deslogo o usuario
    logout(request)
    # redieciono pra página de login
    return redirect('conta:login')



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
            #formUser = RegisterUserForm(request.POST, request.FILES)
            # usuarios inativos
            user = formUser.save(commit=False)
            user.is_active = False
            # pego os dados do formulario
            dados_formUser = formUser.data
            #print(formUser.data)
            # salvo o Abstract User
            user.save()
            # autentico o novo usuario
            #user = authenticate(request, username=dados_formUser['username'], password=dados_formUser['password1'])
            if user is not None:
                #login sucesso
                # dashboard
                messages.success(request, 'Sua conta foi criada com Sucesso !')
                login(request, user)
                return redirect('conta:dashboard')
            return redirect('conta:login')
        else:
            # retorno o formulário vazia se o formulario incorreto
            formulario_Abstract_User = RegisterUserForm()
            return render(request, self.template_name, {'formulario_User': formulario_Abstract_User, 'Erro': True })

class Dashboard(View):
    @login_required(login_url='conta:login')
    def painel(request):
        # passo o usuario e seus dados
        # futuramente passo a estrutura da árvore
        if request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
        return render(request, 'dashboard/index.html', {'perfil_logado': user})
    
    
    @login_required(login_url='conta:login')
    def user_profile(request):
        '''
        Function-Based View para listar os atributos do usuario
        '''
        args = {'user': request.user}
        args.update({'message':messages.get_messages(request)})
        return render(request, 'dashboard/listardados.html', args)
        # outras funcionalidades

    @login_required(login_url='conta:login')
    def edit_user(request):
        '''
        Function-Based View pra editar campos do usuario
        '''
        if request.method == 'POST':
            form = AtualizarUserForm(request.POST, request.FILES, instance=request.user)
            args = {'form': form}
            #print('FORMULARIO POST',form.data)
            if form.is_valid():
                form.save()
                args = {'form': form}
                messages.success(request, 'Seus dados foram atualizados com sucesso!')
                return render(request, 'dashboard/listardados.html', args)
            # erro no form
            else:
                args.update({'erro':True})
                return render(request, 'dashboard/listardados.html', args)
        else:
            form = AtualizarUserForm(instance=request.user)
            #print('FORMULARIO GET',form.data)
            user = request.user
            args = {'form': form,'user': user}
            return render(request, 'dashboard/atualizar.html', args)

    @login_required(login_url='conta:login')
    def edit_password(request):
        if request.method == 'POST':
            form = AtualizarSenhaForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Sua senha foi atualizada com sucesso!')
                return redirect('conta:user_dados')
        else:
            form = AtualizarSenhaForm(request.user)
        return render(request, 'dashboard/atualizar_password.html', {
            'form': form
        })