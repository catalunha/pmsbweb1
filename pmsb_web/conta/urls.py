from django.urls import path
from . import views


urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    
    # create view
    path('registrar/', views.ResgisterUser.as_view(), name='registrar'),
    
    # update views
    path('editarPerfil/', views.Dashboard.edit_user, name="user_edit"),
    path('editarSenha/', views.Dashboard.edit_password, name='user_password'),

    # list view
    path('conta/', views.Dashboard.user_profile, name="user_dados"),
    # listar todos os atributos do perfil do usuário
    path('perfil/', views.AtributoListView.as_view() , name="perfil_list"),
    
    # dashboard view
    path('painel/', views.Dashboard.painel, name='dashboard'),
    
    # perfil
    path('perfil/preencher/<uuid:pk>/', views.ValorAtributoCreateView.as_view(), name='perfil_create'),

    
    # organograma
    #path('organograma/hierarquia/',views.HierarquiaListView.as_view(), name='hierarquia_tree'),
    path('organograma/cargos/',views.CargoListView.as_view(), name='cargo_tree'),
    path('organograma/departamentos/',views.DepartamentoListView.as_view(), name='departamento_tree')

] 
