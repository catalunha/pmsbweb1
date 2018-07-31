
from django.urls import path

app_name = "questionarios"

from . import views

urlpatterns = [

    # questionarios
    path("", views.QuestionarioListView.as_view(), name = "list"),
    path("criar/", views.QuestionarioCreateView.as_view(), name = "create"),
    path("editar/<int:pk>/", views.QuestioanrioUpdateView.as_view(), name = "update"),
    path("ordenar/<int:pk>",views.QuestionarioOrdenarView.as_view(), name = "ordenar"),
    path("delete/<int:pk>/", views.QuestioanrioDeleteView.as_view(), name = "delete"),

    #perguntas
    path("criar/pergunta/tipo/", views.PerguntaEscolherTipoTemplateView.as_view(), name = "create_pergunta_tipo"),
    path("criar/pergunta/<int:pk>/tipo/<int:tipo>/", views.PerguntaCreateView.as_view(), name = "create_pergunta"),
    path("editar/pergunta/<int:pk>/", views.PerguntaUpdateView.as_view(), name = "update_pergunta"),
    path("delete/pergunta/<int:pk>/", views.PerguntaDeleteView.as_view(), name = "delete_pergunta"),
]