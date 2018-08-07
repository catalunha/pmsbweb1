from django.urls import path
from . import views


urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    
    # create view ()
    path('registrar', views.ResgisterUser.as_view(), name='registrar'),
    
    # update views ()
    path('editarPerfil/', views.Dashboard.edit_user, name="user_edit"),
    path('editarSenha/', views.Dashboard.edit_password, name='user_password'),

    # list view ()
    path('perfil', views.Dashboard.user_profile, name="user_dados"),
    
    # dashboard view's
    path('painel', views.Dashboard.painel, name='dashboard'),
    # organograma
    path('organograma/hierarquia',views.Dashboard.hierarquia_tree, name='hierarquia_tree'),
    path('organograma/cargos',views.Dashboard.cargo_tree, name='cargo_tree'),
    path('organograma/departamentos',views.Dashboard.departamento_tree, name='departamento_tree')

] 
