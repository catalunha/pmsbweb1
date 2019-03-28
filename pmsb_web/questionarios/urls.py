
from django.urls import path

app_name = "questionarios"

from . import views

urlpatterns = [

    # questionarios
    path("", views.QuestionarioListView.as_view(), name = "list"),
    path("equipe", views.QuestionarioEquipeListView.as_view(), name = "questionario_list_equipe"),
    path("criar/", views.QuestionarioCreateView.as_view(), name = "create"),
    path("editar/<uuid:pk>/", views.QuestioanrioUpdateView.as_view(), name = "update"),
    path("ordenar/<uuid:pk>",views.QuestionarioOrdenarDetailView.as_view(), name = "ordenar"),
    path("ajax/ordenar/",views.QuestionarioOrdenarSubmitAjaxView.as_view(), name = "ordenar_submit"),
    path("delete/<uuid:pk>/", views.QuestioanrioDeleteView.as_view(), name = "delete"),

    #perguntas
    path("criar/pergunta/tipo/<uuid:pk>/", views.PerguntaEscolherTipoTemplateView.as_view(), name = "create_pergunta_tipo"),
    path("criar/pergunta/<uuid:pk>/tipo/<int:tipo>/", views.PerguntaCreateView.as_view(), name = "create_pergunta"),
    path("editar/pergunta/<uuid:pk>/", views.PerguntaUpdateView.as_view(), name = "update_pergunta"),
    path("delete/pergunta/<uuid:pk>/", views.PerguntaDoQuestionarioDeleteView.as_view(), name = "delete_pergunta_do_questionario"),
    path("perguntas/", views.PerguntaListView.as_view(), name = "pergunta_list"),
    path("pergunta/<uuid:pk>/", views.PerguntaDetailView.as_view(), name = "pergunta_detail"),

    # requisitos
    path("perguntas/perguntarequisito/<uuid:pk>/criar/", views.PerguntaRequisitoCreateView.as_view(),
         name="perguntarequisito_create"),
    path("perguntas/escolharequisito/<uuid:pk>/criar/", views.EscolhaRequisitoCreateView.as_view(),
         name="escolharequisito_create"),

    path("perguntas/perguntarequisito/<uuid:pergunta_do_questionario_pk>/deletar/<uuid:pk>/",
         views.PerguntaRequisitoDeleteView.as_view(), name="perguntarequisito_delete"),
    path("perguntas/escolharequisito/<uuid:pergunta_do_questionario_pk>/deletar/<uuid:pk>/",
         views.EscolhaRequisitoDeleteView.as_view(), name="escolharequisito_delete"),

    path("perguntas/ajax/get_perguntas_do_questionario", views.ajax_get_perguntas_do_questionario,
         name="ajax_get_perguntas_do_questionario"),
    path("perguntas/ajax/get_escolhas_da_pergunta_do_questionario", views.ajax_get_escolhas_da_pergunta_do_questionario,
         name="ajax_get_escolhas_da_pergunta_do_questionario"),

    #possivel escolha
    path("editar/pergunta/<uuid:pk>/criar_escolha", views.PossivelEscolhaCreateView.as_view(), name = "create_possivelescolha"),
    path("editar/pergunta/<uuid:pergunta_questionario_pk>/editar_escolha/<uuid:pk>", views.PossivelEscolhaUpdateView.as_view(), name = "update_possivelescolha"),
    path("editar/pergunta/<uuid:pergunta_questionario_pk>/delete_escolha/<uuid:pk>", views.PossivelEscolhaDeleteView.as_view(), name = "delete_possivelescolha"),

    path("teste/", views.TesteTemplateView.as_view(), name = "teste"),
]