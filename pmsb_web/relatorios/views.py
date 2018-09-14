from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth import get_user_model
from core.views import (
    FakeDeleteView,
    AjaxableFormResponseMixin,
)

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
    BlocoTextoForm,
    BlocoOrdemAjaxForm,
    BlocoSuperiorForm,
    EditorForm,
)

User = get_user_model()

"""
Relatorio
"""

class RelatorioDonoOuEditorQuerysetMixin(object):
    def get_queryset(self, queryset = None):
        queryset = Relatorio.objetcs.by_dono_ou_editor(self.request.user)
        return queryset.fake_delete_all()

class RelatorioDonoQuerysetMixin(object):
    def get_queryset(self, queryset = None):
        queryset = Relatorio.objetcs.fake_delete_all().filter(usuario = self.request.user)
        return queryset

class RelatorioListView(RelatorioDonoOuEditorQuerysetMixin, PermissionRequiredMixin, ListView):
    model = Relatorio
    template_name = "relatorios/list_relatorio.html"
    permission_required = ["relatorios.view_relatorio", ]

class RelatorioDetailView(RelatorioDonoOuEditorQuerysetMixin, PermissionRequiredMixin, DetailView):
    model = Relatorio
    template_name = "relatorios/detail_relatorio.html"
    permission_required = ["relatorios.view_relatorio", ]

    def get_context_data(self, **kwargs):
        context = super(RelatorioDetailView, self).get_context_data(**kwargs)
        relatorio = get_object_or_404(Relatorio, pk = self.kwargs.get("pk"))
        blocos = Bloco.objects.filter(relatorio=relatorio, fake_deletado=False)
        context["blocos_nfd"] = blocos
        return context

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

    success_url = reverse_lazy("relatorios:list_relatorio")

"""
Bloco
"""

class RedirectActionView(SingleObjectMixin, RedirectView):
    model = Bloco

    def action(self):
        pass

    def get(self, request, *args, **kwargs):
        self.get_object()
        self.action()
        return super().get(request, *args, **kwargs)

class BlocoRelatorioContextMixin(object):

    def get_context_data(self, **kwargs):
        context = super(BlocoRelatorioContextMixin, self).get_context_data(**kwargs)
        context["relatorio_object"] = get_object_or_404(Relatorio, pk = self.kwargs.get("pk"))
        return context

class BlocoRelatorioSuccessUrlMixin(object):
    
    def get_success_url(self, bloco=None):
        if bloco is None:
            bloco = Bloco.objects.get(id=self.kwargs.get("pk"))
        return reverse_lazy("relatorios:detail_relatorio", kwargs = {"pk":bloco.relatorio.pk})

class BlocoListView(PermissionRequiredMixin, ListView):
    model = Bloco
    template_name = "relatorios/list_bloco.html"
    permission_required = ["relatorios.view_relatorio", "relatorios.view_bloco" ]

class BlocoDetailView(PermissionRequiredMixin, DetailView):
    model = Bloco
    template_name = "relatorios/detail_bloco.html"
    permission_required = ["relatorios.view_relatorio", "relatorios.view_bloco" ]

class BlocoCreateView(BlocoRelatorioContextMixin, PermissionRequiredMixin, CreateView):
    model = Bloco
    template_name = "relatorios/create_bloco.html"
    form_class = BlocoForm
    permission_required = ["relatorios.view_relatorio", "relatorios.view_bloco", "relatorios.add_bloco" ]
    
    def get_success_url(self):
        return reverse_lazy("relatorios:detail_relatorio", kwargs = {"pk":self.kwargs.get("pk")})
    
    def form_valid(self, form):
        relatorio = get_object_or_404(Relatorio, pk=self.kwargs.get('pk'))
        form.instance.relatorio = relatorio
        nivel_superior_pk = self.kwargs.get("nivel_superior_pk", None)
        nivel_superior = None
        if nivel_superior_pk is not None:
            nivel_superior = get_object_or_404(Bloco, pk = nivel_superior_pk)
        form.instance.nivel_superior = nivel_superior
        return super(BlocoCreateView, self).form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super(BlocoCreateView, self).get_form_kwargs()
        kwargs.update({
            "relatorio_pk": self.kwargs.get("pk"),
        })
        return kwargs

class BlocoUpdateView(BlocoRelatorioSuccessUrlMixin, PermissionRequiredMixin, UpdateView):
    model = Bloco
    template_name = "relatorios/update_bloco.html"
    form_class = BlocoChangeForm
    permission_required = ["relatorios.view_relatorio", "relatorios.view_bloco", "relatorios.change_bloco" ]

class BlocoNivelSuperiorUpdateView(BlocoRelatorioSuccessUrlMixin, PermissionRequiredMixin, UpdateView):
    model = Bloco
    template_name = "relatorios/update_bloco.html"
    form_class = BlocoSuperiorForm
    permission_required = ["relatorios.view_relatorio", "relatorios.view_bloco", "relatorios.change_bloco" ]

    def form_valid(self, form):
        form.instance.nivel_superior = self.object.nivel_superior
        form.instance.muda_nivel_superior(form.instance.nivel_superior)
        return super().form_valid(form)

class BlocoUpOrdemView(BlocoRelatorioSuccessUrlMixin, PermissionRequiredMixin, RedirectView):
    permission_required = ["relatorios.view_relatorio", "relatorios.view_bloco", "relatorios.change_bloco" ]

    def get(self, request, *args ,**kwargs):
        bloco = Bloco.objects.get(pk=self.kwargs.pop("pk"))
        bloco.ordenacao(1)        
        return HttpResponseRedirect(self.get_success_url(bloco))

class BlocoDownOrdemView(BlocoRelatorioSuccessUrlMixin, PermissionRequiredMixin, RedirectView):
    permission_required = ["relatorios.view_relatorio", "relatorios.view_bloco", "relatorios.change_bloco" ]

    def get(self, request, *args ,**kwargs):
        bloco = Bloco.objects.get(pk=self.kwargs.pop("pk"))
        bloco.ordenacao(-1)   
        url = self.get_success_url(bloco)
        return HttpResponseRedirect(url)

class BlocoTextoCreateView(BlocoRelatorioSuccessUrlMixin, PermissionRequiredMixin, UpdateView):
    model = Bloco
    template_name = "relatorios/update_bloco.html"
    form_class = BlocoTextoForm
    permission_required = ["relatorios.view_relatorio", "relatorios.view_bloco", "relatorios.change_bloco" ]

class BlocoDeleteView(BlocoRelatorioSuccessUrlMixin, PermissionRequiredMixin, FakeDeleteView):
    model = Bloco
    template_name = "relatorios/delete_bloco.html"
    permission_required = ["relatorios.view_relatorio", "relatorios.view_bloco", "relatorios.delete_bloco" ]

class BlocoOrdemAjaxUpdateView(AjaxableFormResponseMixin, PermissionRequiredMixin, UpdateView):
    """Modifica atributo ordem do bloco via requisição ajax."""
    model = Bloco
    form_class = BlocoOrdemAjaxForm
    permission_required = ["relatorios.view_relatorio", "relatorios.view_bloco", "relatorios.change_bloco" ]

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
        queryset = Figura.objetcs.filter(usuario = self.request.user, relatorio= self.kwargs.get("relatorio_pk"))
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

"""
Editor
"""
class EditorBlocoContextMixin(object):
    def get_context_data(self, **kwargs):
        context = super(EditorBlocoContextMixin, self).get_context_data(**kwargs)
        context["bloco_object"] = get_object_or_404(Bloco, pk = self.kwargs.get("bloco_pk"))
        return context

class EditorBlocoSuccessUrlMixin(object):
    def get_success_url(self, bloco=None):
        if bloco is None:
            bloco = Bloco.objects.get(id=self.kwargs.get("bloco_pk"))
        return reverse_lazy("relatorios:detail_relatorio", kwargs = {"pk":bloco.relatorio.pk})

class EditorFormKwargs(object):
    def get_form_kwargs(self):
        kwargs = super(EditorFormKwargs, self).get_form_kwargs()
        kwargs.update({ 
            "user": self.request.user,
        })
        return kwargs   

class EditorCreateView(EditorFormKwargs, EditorBlocoContextMixin, EditorBlocoSuccessUrlMixin, PermissionRequiredMixin, CreateView):
    model = Editor
    form_class = EditorForm
    template_name = 'relatorios/create_editor.html'
    permission_required = ["relatorios.view_relatorio", "relatorios.view_bloco", "relatorios.add_editor"]

    def form_valid(self, form):
        bloco = get_object_or_404(Bloco, pk=self.kwargs.get("bloco_pk"))
        if Editor.objects.filter(bloco= bloco, usuario = self.request.user):
            editor = Editor.objects.get(bloco=bloco, usuario=self.request.user)
            bloco.editor = form.instance.editor
            editor.editor = bloco.editor
            bloco.save()
            editor.save()
        else:
            form.instance.bloco = bloco
            form.instance.usuario = self.request.user
            bloco.editor = form.instance.editor
            bloco.save()
            form.save()
        url = self.get_success_url(bloco)
        return HttpResponseRedirect(url)

class EditorUpdateView(EditorFormKwargs, EditorBlocoSuccessUrlMixin, PermissionRequiredMixin, UpdateView):
    model = Editor
    form_class = EditorForm
    template_name = "relatorios/update_editor.html"
    permission_required = ["relatorios.view_relatorio", "relatorios.view_bloco", "relatorios.add_editor", "relatorios.change_editor"]

    def get_object(self, queryset=None):
        print(self.kwargs)
        bloco = Bloco.objects.get(pk=self.kwargs.get("bloco_pk"))
        editor_bloco = User.objects.get(pk=self.kwargs.get("pk")) 
        self.object = Editor.objects.get(bloco_id=bloco, editor_id=editor_bloco)
        return self.object
    
    def form_valid(self, form):
        print("UPDATE")
        bloco = get_object_or_404(Bloco, pk=self.kwargs.get("bloco_pk"))
        editor = Editor.objects.get(bloco=bloco, usuario=self.request.user)
        bloco.editor = form.instance.editor
        editor.editor = bloco.editor
        bloco.save()
        editor.save()
        url = self.get_success_url(bloco)
        return HttpResponseRedirect(url)