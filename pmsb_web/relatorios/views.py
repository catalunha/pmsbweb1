from django.shortcuts import render, get_object_or_404
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
    BlocoChangeForm,
    FiguraForm,
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
    template_name = "relatorios/list_bloco.html"
    permission_required = ["relatorios.view_relatorio", "relatorios.view_bloco" ]

class BlocoDetailView(UserPassesTestMixin, PermissionRequiredMixin, DetailView):
    model = Bloco
    template_name = "relatorios/detail_bloco.html"
    permission_required = ["relatorios.view_relatorio", "relatorios.view_bloco" ]

class BlocoCreateView(PermissionRequiredMixin, CreateView):
    model = Bloco
    template_name = "relatorios/create_bloco.html"
    form_class = BlocoForm
    permission_required = ["relatorios.view_relatorio", "relatorios.view_bloco", "relatorios.add_bloco" ]
    
    success_url = reverse_lazy("relatorios:detail_relatorio")
    
    def form_valid(self, form):
        relatorio = get_object_or_404(Relatorio, id=self.kwargs.get('pk'))
        form.instance.relatorio = relatorio
        return super(BlocoCreateView, self).form_valid(form)


class BlocoUpdateView(UserPassesTestMixin, PermissionRequiredMixin, UpdateView):
    model = Bloco
    template_name = "relatorios/update_bloco.html"
    form_class = BlocoChangeForm
    permission_required = ["relatorios.view_relatorio", "relatorios.view_bloco", "relatorios.change_bloco" ]

class BlocoDeleteView(UserPassesTestMixin, PermissionRequiredMixin, DeleteView):
    model = Bloco
    template_name = "relatorios/delete_bloco.html"
    permission_required = ["relatorios.view_relatorio", "relatorios.view_bloco", "relatorios.delete_bloco" ]



"""
Figura
"""

class FiguraDonoQuerysetMixin(object):
    def get_queryset(self, queryset = None):
        queryset = Figura.objetcs.filter(usuario = self.request.user)
        queryset.filter(relatorio = self.kwargs.get("relatorio_pk"))
        return queryset

class FiguraDonoOuEditorQuerysetMixin(object):
    def get_queryset(self, queryset = None):
        queryset = Figura.objetcs.by_dono_ou_editor(self.request.user)
        queryset.filter(relatorio = self.kwargs.get("relatorio_pk"))
        return queryset

class FiguraRelatorioContextMixin(object):
    def get_context_data(self, **kwargs):
        context = super(FiguraRelatorioContextMixin, self).get_context_data(**kwargs)
        context["relatorio_object"] = get_object_or_404(Relatorio, pk = self.kwargs.get("relatorio_pk"))
        return context

class FiguraListView(FiguraRelatorioContextMixin, FiguraDonoOuEditorQuerysetMixin, PermissionRequiredMixin, ListView):
    model = Figura
    template_name = "relatorios/list_figura.html"
    permission_required = ["relatorios.view_relatorio", "relatorios.view_figura", ]

class FiguraDetailView(FiguraDonoOuEditorQuerysetMixin, PermissionRequiredMixin, DetailView):
    model = Figura
    template_name = "relatorios/detail_figura.html"
    permission_required = ["relatorios.view_relatorio", "relatorios.view_figura", ]

class FiguraCreateView(FiguraRelatorioContextMixin, PermissionRequiredMixin, CreateView):
    model = Figura
    form_class = FiguraForm
    template_name = "relatorios/create_figura.html"
    permission_required = ["relatorios.view_relatorio", "relatorios.view_figura", "relatorios.add_figura" ]

    def get_success_url(self):
        return reverse_lazy("relatorios:list_figura", kwargs = {"relatorio_pk":self.kwargs.get("relatorio_pk")})

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        relatorio = get_object_or_404(Relatorio, pk = self.kwargs.get("relatorio_pk"))
        form.instance.relatorio = relatorio
        return super(FiguraCreateView, self).form_valid(form)

class FiguraUpdateView(FiguraDonoQuerysetMixin, PermissionRequiredMixin, UpdateView):
    model = Figura
    form_class = FiguraForm
    template_name = "relatorios/update_figura.html"
    permission_required = ["relatorios.view_relatorio", "relatorios.view_figura", "relatorios.change_figura" ]

    def get_success_url(self):
        return reverse_lazy("relatorios:list_figura", kwargs = {"relatorio_pk":self.object.relatorio.pk})


class FiguraDeleteView(FiguraDonoQuerysetMixin, PermissionRequiredMixin, DeleteView):
    model = Figura
    template_name = "relatorios/delete_figura.html"
    permission_required = ["relatorios.view_relatorio", "relatorios.view_figura", "relatorios.delete_figura" ]

    def get_success_url(self):
        return reverse_lazy("relatorios:list_figura", kwargs = {"relatorio_pk":self.object.relatorio.pk})

