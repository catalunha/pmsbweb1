from django.urls import path

app_name = "relatorios"

from . import views

urlpatterns = [

    # relatorios
    path("", views.RelatorioListView.as_view(), name = "list_relatorio"),
    path("novo/", views.RelatorioCreateView.as_view(), name = "create_relatorio"),
    path("<uuid:pk>/ver", views.RelatorioDetailView.as_view(), name = "detail_relatorio"),
    path("<uuid:pk>/editar", views.RelatorioUpdateView.as_view(), name = "update_relatorio"),
    path("<uuid:pk>/deletar", views.RelatorioDetailView.as_view(), name = "delete_relatorio"),

    #blocos
    path("<uuid:pk>/bloco", views.BlocoCreateView.as_view(), name="create_bloco"),

    #figuras
    path("<uuid:relatorio_pk>/figuras/", views.FiguraListView.as_view(), name = "list_figura"),
    path("figuras/<uuid:pk>", views.FiguraDetailView.as_view(), name = "detail_figura"),
    path("<uuid:relatorio_pk>/figuras/nova", views.FiguraCreateView.as_view(), name = "create_figura"),
    path("figuras/<uuid:pk>/editar", views.FiguraUpdateView.as_view(), name = "update_figura"),
    path("figuras/<uuid:pk>/delete", views.FiguraDeleteView.as_view(), name = "delete_figura"),
]