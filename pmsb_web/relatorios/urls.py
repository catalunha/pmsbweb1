from django.urls import path

app_name = "relatorios"

from . import views

urlpatterns = [

    # relatorios
    path("", views.RelatorioListView.as_view(), name = "list_relatorio"),
    path("novo/", views.RelatorioCreateView.as_view(), name = "create_relatorio"),
    path("<uuid:pk>/ver/", views.RelatorioDetailView.as_view(), name = "detail_relatorio"),
    path("<uuid:pk>/editar/", views.RelatorioUpdateView.as_view(), name = "update_relatorio"),
    path("<uuid:pk>/deletar/", views.RelatorioDeleteView.as_view(), name = "delete_relatorio"),
    

    #blocos
    path("<uuid:pk>/bloco/", views.BlocoCreateView.as_view(), name="create_bloco"),
    path("<uuid:pk>/bloco/<uuid:nivel_superior_pk>/", views.BlocoCreateView.as_view(), name="create_bloco_nivel_superior"),
    path("bloco/<uuid:pk>/editar/", views.BlocoUpdateView.as_view(), name="update_bloco"),
    path("bloco/<uuid:pk>/nivel_superior/editar/", views.BlocoNivelSuperiorUpdateView.as_view(), name="update_bloco_nivel_superior"),
    path("bloco/<uuid:pk>/subir", views.BlocoUpOrdemView.as_view(), name="subir_bloco"),
    path("bloco/<uuid:pk>/descer", views.BlocoDownOrdemView.as_view(), name="descer_bloco"),
    path("bloco/<uuid:pk>/texto/", views.BlocoTextoCreateView.as_view(), name="update_text_bloco"),
    path("bloco/<uuid:pk>/deletar/", views.BlocoDeleteView.as_view(), name="delete_bloco"),

    # editor
    path("bloco/<uuid:pk>/editor/", views.EditorUpdateView.as_view(), name="update_editor_bloco"),

    #blocos ajax
    path("ajax/bloco/<uuid:pk>/editar/", views.BlocoOrdemAjaxUpdateView.as_view(), name="ajax_update_bloco"),

    #figuras
    path("<uuid:relatorio_pk>/figuras/", views.FiguraListView.as_view(), name = "list_figura"),
    path("figuras/<uuid:pk>/", views.FiguraDetailView.as_view(), name = "detail_figura"),
    path("<uuid:relatorio_pk>/figuras/nova/", views.FiguraCreateView.as_view(), name = "create_figura"),
    path("figuras/<uuid:pk>/editar/", views.FiguraUpdateView.as_view(), name = "update_figura"),
    path("figuras/<uuid:pk>/delete/", views.FiguraDeleteView.as_view(), name = "delete_figura"),
]