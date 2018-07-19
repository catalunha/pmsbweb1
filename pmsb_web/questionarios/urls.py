
from django.urls import path

app_name = "questionarios"

from . import views

urlpatterns = [
    path("teste/", views.TesteView.as_view(), name = "teste"),  
]