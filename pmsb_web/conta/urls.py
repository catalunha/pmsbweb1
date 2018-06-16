from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('registrar', views.ResgisterUser.as_view(), name='registrar'),
    
    # update views ()
    
    
    
    # dashboard view's
    path('painel', views.Dashboard.painel, name='dashboard'),

]
