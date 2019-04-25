from core.views import (
    FakeDeleteView,
    AjaxableFormResponseMixin,
    FakeDeleteQuerysetViewMixin
)
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from django.views.generic.detail import SingleObjectMixin

from .forms import (
    RelatorioForm,
    BlocoForm,
    BlocoChangeForm,
    FiguraForm,
    BlocoTextoForm,
    BlocoOrdemAjaxForm,
    BlocoSuperiorForm,
    EditorUpdateForm,
)
from .models import (
    Relatorio,
    Bloco,
    Figura,
)

User = get_user_model()

"""
Relatorio
"""


class RelatorioDonoOuEditorQuerysetMixin(object):
    def get_queryset(self, queryset=None):
        queryset = Relatorio.objects.by_dono_ou_editor(self.request.user)
        return queryset.fake_delete_all().distinct()


class RelatorioDonoQuerysetMixin(object):
    def get_queryset(self, queryset=None):
        queryset = Relatorio.objects.fake_delete_all().filter(usuario=self.request.user)
        return queryset.distinct()


class RelatorioDonoEditorSuperiorQuerysetMixin(object):
    def get_queryset(self, queryset=None):
        queryset = super().get_queryset()
        superior_queryset = queryset.by_superior(self.request.user)
        superior_queryset = superior_queryset.fake_delete_all()
        queryset = queryset.by_dono_ou_editor(self.request.user)
        queryset = queryset | superior_queryset
        return queryset.fake_delete_all().distinct()


class RelatorioListView(RelatorioDonoEditorSuperiorQuerysetMixin, PermissionRequiredMixin, ListView):
    model = Relatorio
    template_name = "relatorios/list_relatorio.html"
    permission_required = ["relatorios.view_relatorio", ]


class RelatorioDetailView(RelatorioDonoEditorSuperiorQuerysetMixin, PermissionRequiredMixin, DetailView):
    model = Relatorio
    template_name = "relatorios/detail_relatorio.html"
    permission_required = ["relatorios.view_relatorio", ]

    def get_context_data(self, **kwargs):
        context = super(RelatorioDetailView, self).get_context_data(**kwargs)
        relatorio = get_object_or_404(Relatorio, pk=self.kwargs.get("pk"))
        blocos = Bloco.objects.filter(relatorio=relatorio, fake_deletado=False)
        context["blocos_nfd"] = blocos
        return context


class RelatorioCreateView(PermissionRequiredMixin, CreateView):
    model = Relatorio
    form_class = RelatorioForm
    template_name = "relatorios/create_relatorio.html"
    permission_required = [
        "relatorios.view_relatorio", "relatorios.add_relatorio"]

    success_url = reverse_lazy("relatorios:list_relatorio")

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super(RelatorioCreateView, self).form_valid(form)


class RelatorioUpdateView(RelatorioDonoQuerysetMixin, PermissionRequiredMixin, UpdateView):
    model = Relatorio
    form_class = RelatorioForm
    template_name = "relatorios/update_relatorio.html"
    permission_required = ["relatorios.view_relatorio",
                           "relatorios.change_relatorio"]

    success_url = reverse_lazy("relatorios:list_relatorio")


class RelatorioDeleteView(RelatorioDonoQuerysetMixin, PermissionRequiredMixin, FakeDeleteQuerysetViewMixin,
                          FakeDeleteView):
    model = Relatorio
    template_name = "relatorios/delete_relatorio.html"
    permission_required = ["relatorios.view_relatorio",
                           "relatorios.delete_relatorio"]

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
        context = super(BlocoRelatorioContextMixin,
                        self).get_context_data(**kwargs)
        context["relatorio_object"] = get_object_or_404(
            Relatorio, pk=self.kwargs.get("pk"))
        return context


class BlocoRelatorioSuccessUrlMixin(object):

    def get_success_url(self, bloco=None):
        if bloco is None:
            bloco = Bloco.objects.get(id=self.kwargs.get("pk"))
        return reverse_lazy("relatorios:detail_relatorio", kwargs={"pk": bloco.relatorio.pk})


class BlocoListView(PermissionRequiredMixin, ListView):
    model = Bloco
    template_name = "relatorios/list_bloco.html"
    permission_required = [
        "relatorios.view_relatorio", "relatorios.view_bloco"]


class BlocoDetailView(PermissionRequiredMixin, DetailView):
    model = Bloco
    template_name = "relatorios/detail_bloco.html"
    permission_required = [
        "relatorios.view_relatorio", "relatorios.view_bloco"]


class BlocoCreateView(BlocoRelatorioContextMixin, PermissionRequiredMixin, CreateView):
    model = Bloco
    template_name = "relatorios/create_bloco.html"
    form_class = BlocoForm
    permission_required = ["relatorios.view_relatorio",
                           "relatorios.view_bloco", "relatorios.add_bloco"]

    def get_success_url(self):
        return reverse_lazy("relatorios:detail_relatorio", kwargs={"pk": self.kwargs.get("pk")})

    def form_valid(self, form):
        relatorio = get_object_or_404(Relatorio, pk=self.kwargs.get('pk'))
        form.instance.relatorio = relatorio
        nivel_superior_pk = self.kwargs.get("nivel_superior_pk", None)
        nivel_superior = None
        if nivel_superior_pk is not None:
            nivel_superior = get_object_or_404(Bloco, pk=nivel_superior_pk)
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
    permission_required = ["relatorios.view_relatorio",
                           "relatorios.view_bloco", "relatorios.change_bloco"]


class BlocoNivelSuperiorUpdateView(BlocoRelatorioSuccessUrlMixin, PermissionRequiredMixin, UpdateView):
    model = Bloco
    template_name = "relatorios/update_bloco.html"
    form_class = BlocoSuperiorForm
    permission_required = ["relatorios.view_relatorio",
                           "relatorios.view_bloco", "relatorios.change_bloco"]

    def form_valid(self, form):
        form.instance.nivel_superior = self.object.nivel_superior
        form.instance.muda_nivel_superior(form.instance.nivel_superior)
        return super().form_valid(form)


class BlocoUpOrdemView(BlocoRelatorioSuccessUrlMixin, PermissionRequiredMixin, RedirectView):
    permission_required = ["relatorios.view_relatorio",
                           "relatorios.view_bloco", "relatorios.change_bloco"]

    def get(self, request, *args, **kwargs):
        bloco = Bloco.objects.get(pk=self.kwargs.pop("pk"))
        bloco.ordenacao(1)
        return HttpResponseRedirect(self.get_success_url(bloco))


class BlocoDownOrdemView(BlocoRelatorioSuccessUrlMixin, PermissionRequiredMixin, RedirectView):
    permission_required = ["relatorios.view_relatorio",
                           "relatorios.view_bloco", "relatorios.change_bloco"]

    def get(self, request, *args, **kwargs):
        bloco = Bloco.objects.get(pk=self.kwargs.pop("pk"))
        bloco.ordenacao(-1)
        url = self.get_success_url(bloco)
        return HttpResponseRedirect(url)


class BlocoTextoCreateView(BlocoRelatorioSuccessUrlMixin, PermissionRequiredMixin, UpdateView):
    model = Bloco
    template_name = "relatorios/update_bloco.html"
    form_class = BlocoTextoForm
    permission_required = ["relatorios.view_relatorio",
                           "relatorios.view_bloco", "relatorios.change_bloco"]


class BlocoDeleteView(BlocoRelatorioSuccessUrlMixin, PermissionRequiredMixin, FakeDeleteView):
    model = Bloco
    template_name = "relatorios/delete_bloco.html"
    permission_required = ["relatorios.view_relatorio",
                           "relatorios.view_bloco", "relatorios.delete_bloco"]


class BlocoOrdemAjaxUpdateView(AjaxableFormResponseMixin, PermissionRequiredMixin, UpdateView):
    """Modifica atributo ordem do bloco via requisição ajax."""
    model = Bloco
    form_class = BlocoOrdemAjaxForm
    permission_required = ["relatorios.view_relatorio",
                           "relatorios.view_bloco", "relatorios.change_bloco"]


"""
Figura
"""


class FiguraDonoQuerysetMixin(object):
    def get_queryset(self, queryset=None):
        queryset = Figura.objects.filter(usuario=self.request.user)
        queryset.filter(relatorio=self.kwargs.get("relatorio_pk"))
        return queryset


class FiguraDonoOuEditorQuerysetMixin(object):
    def get_queryset(self, queryset=None):
        queryset = Figura.objects.filter(
            usuario=self.request.user, relatorio=self.kwargs.get("relatorio_pk"))
        return queryset


class FiguraRelatorioContextMixin(object):
    def get_context_data(self, **kwargs):
        context = super(FiguraRelatorioContextMixin,
                        self).get_context_data(**kwargs)
        context["relatorio_object"] = get_object_or_404(
            Relatorio, pk=self.kwargs.get("relatorio_pk"))
        return context


class FiguraListView(FiguraRelatorioContextMixin, FiguraDonoOuEditorQuerysetMixin, PermissionRequiredMixin, ListView):
    model = Figura
    template_name = "relatorios/list_figura.html"
    permission_required = [
        "relatorios.view_relatorio", "relatorios.view_figura", ]


class FiguraDetailView(FiguraDonoOuEditorQuerysetMixin, PermissionRequiredMixin, DetailView):
    model = Figura
    template_name = "relatorios/detail_figura.html"
    permission_required = [
        "relatorios.view_relatorio", "relatorios.view_figura", ]


class FiguraCreateView(FiguraRelatorioContextMixin, PermissionRequiredMixin, CreateView):
    model = Figura
    form_class = FiguraForm
    template_name = "relatorios/create_figura.html"
    permission_required = ["relatorios.view_relatorio",
                           "relatorios.view_figura", "relatorios.add_figura"]

    def get_success_url(self):
        return reverse_lazy("relatorios:list_figura", kwargs={"relatorio_pk": self.kwargs.get("relatorio_pk")})

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        relatorio = get_object_or_404(
            Relatorio, pk=self.kwargs.get("relatorio_pk"))
        form.instance.relatorio = relatorio
        return super(FiguraCreateView, self).form_valid(form)


class FiguraUpdateView(FiguraDonoQuerysetMixin, PermissionRequiredMixin, UpdateView):
    model = Figura
    form_class = FiguraForm
    template_name = "relatorios/update_figura.html"
    permission_required = ["relatorios.view_relatorio",
                           "relatorios.view_figura", "relatorios.change_figura"]

    def get_success_url(self):
        return reverse_lazy("relatorios:list_figura", kwargs={"relatorio_pk": self.object.relatorio.pk})


class FiguraDeleteView(FiguraDonoQuerysetMixin, PermissionRequiredMixin, DeleteView):
    model = Figura
    template_name = "relatorios/delete_figura.html"
    permission_required = ["relatorios.view_relatorio",
                           "relatorios.view_figura", "relatorios.delete_figura"]

    def get_success_url(self):
        return reverse_lazy("relatorios:list_figura", kwargs={"relatorio_pk": self.object.relatorio.pk})


"""
Editor
"""


class EditorUpdateView(PermissionRequiredMixin, UpdateView):
    model = Bloco
    form_class = EditorUpdateForm
    template_name = "relatorios/update_editor.html"
    permission_required = ["relatorios.view_relatorio",
                           "relatorios.view_bloco", "relatorios.change_bloco"]

    def get_success_url(self):
        return reverse_lazy("relatorios:detail_relatorio", kwargs={"pk": self.object.relatorio.pk})


"""Render PDF"""
import os
from django.http import Http404
from django.shortcuts import render
from .models import TemplateLatex, TemplateLatexRelatorio, Bibtex
from django.conf import settings
from subprocess import call
from django.template import Template, Context
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.files.storage import default_storage
import shutil


def render_pdf(request, pk):
    relatorio = get_object_or_404(Relatorio, pk=pk)

    templates_latex: TemplateLatexRelatorio = relatorio.templatelatexrelatorio

    if not hasattr(relatorio, 'templatelatexrelatorio'):
        raise Http404

    template_relatorio: TemplateLatex = templates_latex.template_relatorio

    bibs = Bibtex.objects.all()

    blocos = Bloco.objects.filter(relatorio=relatorio)

    context = {
        'bibtex': bibs,
        'relatorio': relatorio,
        'blocos': blocos,
    }

    relatorio_dir = os.path.join(settings.TEMP_DIR, f"{pk}")
    os.makedirs(relatorio_dir, exist_ok=True)

    tex_filename = f"{relatorio_dir}/{pk}.tex"
    pdf_filename = f"{relatorio_dir}/{pk}.pdf"
    aux_filename = f"{relatorio_dir}/{pk}.aux"
    toc_filename = f"{relatorio_dir}/{pk}.toc"
    log_filename = f"{relatorio_dir}/{pk}.log"

    RELATORIOS_MEDIA = os.path.join(settings.MEDIA_ROOT, 'relatorios')
    RELATORIOS_MEDIA_PDF = os.path.join(RELATORIOS_MEDIA, 'pdfs')

    with template_relatorio.arquivo.open(mode='r') as f:
        template_relatorio_conteudo = f.read()

    t = Template(template_relatorio_conteudo)
    c = Context(context)
    tex_content = t.render(c)

    with open(tex_filename, 'w', encoding='utf-8') as f:
        f.write(tex_content)

    call(["pdflatex", "-interaction", "nonstopmode", tex_filename], cwd=relatorio_dir)

    storage_filename = os.path.join(RELATORIOS_MEDIA_PDF, f'{pk}.pdf')
    image_temp_file = NamedTemporaryFile(delete=True)

    with open(pdf_filename, mode='rb') as f:
        image_temp_file.write(f.read())

    image_temp_file.flush()
    temp_file = File(name="outro-nome.pdf", file=image_temp_file)
    default_storage.delete(storage_filename)
    default_storage.save(storage_filename, temp_file)

    #shutil.rmtree(relatorio_dir, ignore_errors=True)  # remove todos os arquivos gerados

    return render(request, 'relatorios/render_pdf.html', context)
