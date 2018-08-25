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
]