# encoding: utf-8
# django imports
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
)
from django.views.generic.base import View
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin
# project imports
from .forms import (
    RegisterUserForm,
    AtualizarUserForm,
    AtualizarSenhaForm,
    BaseDocumentoAtributoForm,
    BaseValorAtributoForm,
)
from .models import (
    User,
    Atributo,
    Departamento,
    Cargo,
    ValorAtributo,
    DocumentoAtributo,
)
import collections
from django.utils import timezone

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
            new_user = formUser.save(commit=False)
            new_user.is_active = False
            # pego os dados do formulario
            dados_formUser = formUser.data
            #print(formUser.data)
            # salvo o Abstract User
            new_user.save()
            # autentico o novo usuario
            user = authenticate(request, username=dados_formUser['username'], password=dados_formUser['password1'])
            if user is not None:
                #login sucesso
                # dashboard
                messages.success(request, 'Sua conta foi criada com Sucesso !')
                login(request, user)
                return redirect('conta:dashboard')
            # passar pra view de sucesso no cadastro
            return render(request, 'conta/sucess.html', {'new_user':new_user})
        else:
            # retorno o formulário vazia se o formulario incorreto
            formulario_Abstract_User = formUser
            return render(request, self.template_name, {'formulario_User': formulario_Abstract_User })

class Dashboard(PermissionRequiredMixin, View):
    def painel(request):
        # passo o usuario e seus dados
        # futuramente passo a estrutura da árvore
        if request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
        return render(request, 'dashboard/index.html', {'perfil_logado': user})
    
    def user_profile(request):
        '''
        Function-Based View para listar os atributos do usuario
        '''
        args = {'user': request.user}
        args.update({'message':messages.get_messages(request)})
        return render(request, 'dashboard/listardados.html', args)
        # outras funcionalidades

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

"""
    List view dos Organogramas
"""
class UserFilteringQuerySet(object):
    def get_queryset(self):
        return User.objects.filter(is_active=True)
    
class UserContextData(object):
    def get_context_data(self, **kwargs):
        context = super(UserContextData, self).get_context_data(**kwargs)
        context.update({
            'all_user_active': User.objects.filter(is_active=True),
            'all_user_not_active': User.objects.all(),
        })
        return context

class HierarquiaListView(UserContextData, UserFilteringQuerySet, PermissionRequiredMixin, ListView):
    template_name = 'dashboard/organograma.html'
    context_object_name = 'hierarquia'
    model = User    
    permission_required = ["conta.view_user"]

class DepartamentoListView(PermissionRequiredMixin, ListView):
    template_name = 'dashboard/organograma.html'
    context_object_name = 'departamentos'
    model = Departamento
    permission_required = ["conta.view_departamento"]

class CargoListView(UserContextData, PermissionRequiredMixin, ListView):
    template_name = 'dashboard/organograma.html'
    context_object_name = 'cargolist'
    model = Departamento
    permission_required = ["conta.view_departamento"]

"""
    Views dos Atributos/ValorAtriutos do Perfil
"""
class AtributoListView(ListView):
    template_name = 'dashboard/perfil_list.html'
    context_object_name = 'atributos'
    model = Atributo

    def get_context_data(self, **kwargs):
        context = super(AtributoListView, self).get_context_data(**kwargs)
        # todos atributos
        atributos = self.get_queryset()
        lista = []
        check_valor = collections.namedtuple('check', 'atributo isPreenchido')
        # checo pra cada atributo se o meu usuário o preencheu pra atualizar o contexto da ListView
        for atributo in atributos:
            if atributo.valor == True:
                valor = check_valor(atributo=atributo, 
                isPreenchido=ValorAtributo.objects.filter(usuario=self.request.user, tipo=atributo))
                lista.append(valor)
            elif atributo.documento == True:    
                documento = check_valor(atributo=atributo, 
                isPreenchido=DocumentoAtributo.objects.filter(usuario=self.request.user, tipo=atributo))
                lista.append(documento)
            elif atributo.valor == atributo.documento:
                valor_documento = check_valor(atributo=atributo, 
                isPreenchido=ValorAtributo.objects.filter(usuario=self.request.user, tipo=atributo)+DocumentoAtributo.objects.filter(usuario=self.request.user, tipo=atributo))
                lista.append(valor_documento)
        context.update({
            'atributos': lista,
        })
        return context

# trocar esta joça feia
class ValorAtributoCreateView(CreateView):
    template_name = 'dashboard/perfil_form.html'

    def get_atributo(self):
        return Atributo.objects.get(id=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        """
        TODO: refatorar, codigo vai contra a classe que está herdando
        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)
        context['atributo'] = self.get_atributo()
        return context

    def get(self, request, *args, **kwargs):
        atributo = self.get_atributo()
        #valoratributo = ValorAtributo.objects.get(tipo=atributo.id, usuario=self.request.user)
        if atributo.valor == atributo.documento:
            formValor = BaseValorAtributoForm() 
            formDocumento = BaseDocumentoAtributoForm()
            return render(request, self.template_name, {'args':atributo, 'formValor': formValor, 'formDocumento':formDocumento})
        elif atributo.valor == True:
            formValor = BaseValorAtributoForm()
            return render(request, self.template_name, {'args':atributo, 'formValor': formValor})
        elif atributo.documento == True:
            formDocumento = BaseDocumentoAtributoForm()
            return render(request, self.template_name, {'args':atributo, 'formValor': formDocumento})

    def post(self, request, *args, **kwargs):
        atributo = self.get_atributo()
        if atributo.valor == atributo.documento:
            formValor = BaseValorAtributoForm(request.POST)
            formDocumento = BaseDocumentoAtributoForm(request.POST, request.FILES)
            if formValor.is_valid() and formDocumento.is_valid():
                try:
                    ValorAtributo.objects.filter(tipo=atributo, usuario=self.request.user).update(valor=formValor.data['valor'],editado_em=timezone.now())
                    documento = DocumentoAtributo.objects.filter(tipo=atributo, usuario=self.request.user)
                    a = BaseDocumentoAtributoForm(request.POST, request.FILES, instance=documento[0])
                    a.save()
                    return redirect('conta:perfil_list')
                except ObjectDoesNotExist:
                    valor = formValor.save(commit=False)
                    documento = formDocumento.save(commit=False)
                    valor.tipo_id = atributo.id
                    valor.usuario_id = self.request.user.id
                    documento.tipo_id = atributo.id
                    documento.usuario_id = self.request.user.id
                    valor.save()
                    documento.save()
                    return redirect('conta:perfil_list')
        elif atributo.valor == True:
            print("atributo valor = True")
            formValor = BaseValorAtributoForm(request.POST)
            if formValor.is_valid():
                try:
                    ValorAtributo.objects.get(tipo=atributo,usuario=self.request.user)
                    ValorAtributo.objects.filter(tipo=atributo, usuario=self.request.user).update(valor=formValor.data['valor'])
                    print("registro ja existe")
                    return redirect('conta:perfil_list')
                except ObjectDoesNotExist:
                    data = formValor.save(commit=False)
                    data.tipo = atributo
                    data.usuario = self.request.user
                    data.save()
                    return redirect('conta:perfil_list')
        elif atributo.documento == True:
            formDocumento = BaseDocumentoAtributoForm(request.POST, request.FILES)
            if formDocumento.is_valid():
                try:
                    instance = DocumentoAtributo.objects.get(tipo=atributo, usuario=self.request.user)
                    documento = BaseDocumentoAtributoForm(request.POST, request.FILES, instance=instance)
                    documento.save()
                    return redirect('conta:perfil_list')
                except ObjectDoesNotExist:
                    documento = formDocumento.save(commit=False)
                    documento.tipo_id = atributo.id
                    documento.usuario_id = self.request.user.id
                    documento.save()
                    return redirect('conta:perfil_list')    
