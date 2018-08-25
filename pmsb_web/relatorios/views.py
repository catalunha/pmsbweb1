from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin

from core.views import FakeDeleteView

from .models import (
    Relatorio,
    Bloco,
    Editor,
    Figura,
)

from .forms import (
    RelatorioForm,
    BlocoForm,
)

"""
Relatorio
"""

class RelatorioDonoOuEditorQuerysetMixin(object):
    def get_queryset(self, queryset = None):
        queryset = Relatorio.objetcs.by_dono_ou_editor(self.request.user)
        return queryset

class RelatorioDonoQuerysetMixin(object):
    def get_queryset(self, queryset = None):
        queryset = Relatorio.objetcs.filter(usuario = self.request.user)
        return queryset

class RelatorioListView(RelatorioDonoOuEditorQuerysetMixin, PermissionRequiredMixin, ListView):
    model = Relatorio
    template_name = "relatorios/list_relatorio.html"
    permission_required = ["relatorios.view_relatorio", ]

class RelatorioDetailView(RelatorioDonoOuEditorQuerysetMixin, PermissionRequiredMixin, DetailView):
    model = Relatorio
    template_name = "relatorios/detail_relatorio.html"
    permission_required = ["relatorios.view_relatorio", ]

class RelatorioCreateView(PermissionRequiredMixin, CreateView):
    model = Relatorio
    form_class = RelatorioForm
    template_name = "relatorios/create_relatorio.html"
    permission_required = ["relatorios.view_relatorio", "relatorios.add_relatorio" ]

    success_url = reverse_lazy("relatorios:list_relatorio")

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super(RelatorioCreateView, self).form_valid(form)

class RelatorioUpdateView(RelatorioDonoQuerysetMixin, PermissionRequiredMixin, UpdateView):
    model = Relatorio
    form_class = RelatorioForm
    template_name = "relatorios/update_relatorio.html"
    permission_required = ["relatorios.view_relatorio", "relatorios.change_relatorio"]

    success_url = reverse_lazy("relatorios:list_relatorio")

class RelatorioDeleteView(RelatorioDonoQuerysetMixin, PermissionRequiredMixin, FakeDeleteView):
    model = Relatorio
    template_name = "relatorios/delete_relatorio.html"
    permission_required = ["relatorios.view_relatorio", "relatorios.delete_relatorio"]

"""
Bloco
"""

class BlocoListView(UserPassesTestMixin, PermissionRequiredMixin, ListView):
    model = Bloco
    permission_required = ["relatorios.view_relatorio", "relatorios.view_bloco" ]

class BlocoDetailView(UserPassesTestMixin, PermissionRequiredMixin, DetailView):
    model = Bloco
    permission_required = ["relatorios.view_relatorio", "relatorios.view_bloco" ]

class BlocoCreateView(UserPassesTestMixin, PermissionRequiredMixin, CreateView):
    model = Bloco
    permission_required = ["relatorios.view_relatorio", "relatorios.view_bloco", "relatorios.add_bloco" ]

class BlocoUpdateView(UserPassesTestMixin, PermissionRequiredMixin, UpdateView):
    model = Bloco
    permission_required = ["relatorios.view_relatorio", "relatorios.view_bloco", "relatorios.change_bloco" ]

class BlocoDeleteView(UserPassesTestMixin, PermissionRequiredMixin, DeleteView):
    model = Bloco
    permission_required = ["relatorios.view_relatorio", "relatorios.view_bloco", "relatorios.delete_bloco" ]



"""
Figura
"""

class FiguraListView(UserPassesTestMixin, PermissionRequiredMixin, ListView):
    model = Figura
    permission_required = ["relatorios.view_relatorio", "relatorios.view_figura", ]

class FiguraDetailView(UserPassesTestMixin, PermissionRequiredMixin, DetailView):
    model = Figura
    permission_required = ["relatorios.view_relatorio", "relatorios.view_figura", ]

class FiguraCreateView(UserPassesTestMixin, PermissionRequiredMixin, CreateView):
    model = Figura
    permission_required = ["relatorios.view_relatorio", "relatorios.view_figura", "relatorios.add_figura" ]

class FiguraUpdateView(UserPassesTestMixin, PermissionRequiredMixin, UpdateView):
    model = Figura
    permission_required = ["relatorios.view_relatorio", "relatorios.view_figura", "relatorios.change_figura" ]

class FiguraDeleteView(UserPassesTestMixin, PermissionRequiredMixin, DeleteView):
    model = Figura
    permission_required = ["relatorios.view_relatorio", "relatorios.view_figura", "relatorios.delete_figura" ]
