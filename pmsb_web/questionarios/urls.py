
from django.urls import path

app_name = "questionarios"

from . import views

urlpatterns = [

    # questionarios
    path("", views.QuestionarioListView.as_view(), name = "list"),
    path("criar/", views.QuestionarioCreateView.as_view(), name = "create"),
    path("editar/<uuid:pk>/", views.QuestioanrioUpdateView.as_view(), name = "update"),
    path("ordenar/<uuid:pk>",views.QuestionarioOrdenarDetailView.as_view(), name = "ordenar"),
    path("delete/<uuid:pk>/", views.QuestioanrioDeleteView.as_view(), name = "delete"),

    #perguntas
    path("criar/pergunta/tipo/<uuid:pk>/", views.PerguntaEscolherTipoTemplateView.as_view(), name = "create_pergunta_tipo"),
    path("criar/pergunta/<uuid:pk>/tipo/<int:tipo>/", views.PerguntaCreateView.as_view(), name = "create_pergunta"),
    path("editar/<uuid:questionario_pk>/pergunta/<uuid:pk>/", views.PerguntaUpdateView.as_view(), name = "update_pergunta"),
    path("delete/pergunta/<uuid:pk>/", views.PerguntaDoQuestionarioDeleteView.as_view(), name = "delete_pergunta_do_questionario"),

    #possivel escolha
    path("editar/pergunta/<uuid:pk>/criar_escolha", views.PossivelEscolhaCreateView.as_view(), name = "create_possivelescolha"),
    path("editar/pergunta/<uuid:pergunta_pk>/editar_escolha/<uuid:pk>", views.PossivelEscolhaUpdateView.as_view(), name = "update_possivelescolha"),
    path("editar/pergunta/<uuid:pergunta_pk>/delete_escolha/<uuid:pk>", views.PossivelEscolhaDeleteView.as_view(), name = "delete_possivelescolha"),

    path("teste/", views.TesteTemplateView.as_view(), name = "teste"),
]