from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
    TemplateView,
    FormView,
)
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin

from .models import (
    Questionario,
    Pergunta,
    PerguntaArquivo,
    PerguntaCoordenada,
    PerguntaEscolha,
    PerguntaImagem,
    PerguntaNumero,
    PerguntaTexto,
    PerguntaDoQuestionario,
    PossivelEscolha,
)
from .forms import (
    QuestionarioForm,
    BasePerguntaForm,
    QuestionarioDeleteForm,
    PerguntaArquivoForm,
    PerguntaCoordenadaForm,
    PerguntaEscolhaForm,
    PerguntaImagemForm,
    PerguntaNumeroForm,
    PerguntaTextoForm,
    PossivelEscolhaForm,
    PerguntaRequisitoHiddenChangeForm,
)

"""Questionario"""
class QuestionarioListView(PermissionRequiredMixin, ListView):
    model = Questionario
    template_name = "questionarios/list_questionario.html"
    permission_required = ["questionarios.view_questionario"]

    def get_queryset(self):
        queryset = super(QuestionarioListView, self).get_queryset()
        return queryset.filter(usuario = self.request.user)


class QuestionarioEquipeListView(PermissionRequiredMixin, ListView):
    model = Questionario
    template_name = "questionarios/list_questionario_equipe.html"
    permission_required = ["questionarios.view_questionario"]

    def get_queryset(self):
        return Questionario.objects.get_by_superior(self.request.user)

class QuestionarioCreateView(PermissionRequiredMixin, CreateView):
    model = Questionario
    form_class = QuestionarioForm
    template_name = "questionarios/create_questionario.html"
    permission_required = ["questionarios.add_questionario"]
    success_url = reverse_lazy("questionarios:list")

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super(QuestionarioCreateView, self).form_valid(form)

class QuestioanrioUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = "questionarios/update_questionario.html"
    model = Questionario
    form_class = QuestionarioForm
    permission_required = ["questionarios.change_questionario"]
    success_url = reverse_lazy("questionarios:list")

class QuestioanrioDeleteView(PermissionRequiredMixin, FormMixin, DeleteView):
    template_name = "questionarios/delete_questionario.html"
    model = Questionario
    form_class = QuestionarioDeleteForm
    success_url = reverse_lazy("questionarios:list")
    permission_required = ["questionarios.delete_questionario"]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        form.object_id = self.kwargs.get("pk")
        if form.is_valid():
            return super(QuestioanrioDeleteView, self).post(request, *args, **kwargs)
        else:
            return self.form_invalid(form)

class QuestionarioOrdenarDetailView(PermissionRequiredMixin, DetailView):
    model = Questionario
    template_name = "questionarios/ordenar_detail.html"
    permission_required = ["questionarios.change_questionario"]

class QuestionarioOrdenarSubmitAjaxView(PermissionRequiredMixin, View):
    template_name = "questionarios/ordenar_detail.html"
    permission_required = ["questionarios.change_questionario"]

    def get(self, request, *args, **kwargs):
        uuid = self.request.GET.get("id")
        ordem = self.request.GET.get("ordem")
        pergunta_do_questionario = get_object_or_404(PerguntaDoQuestionario, pk = uuid)
        pergunta_do_questionario.ordem = ordem
        pergunta_do_questionario.save()
        return JsonResponse({"id":uuid})

"""Pergunta"""
class PerguntaEscolherTipoTemplateView(PermissionRequiredMixin, DetailView):
    model = Questionario
    template_name = "questionarios/escolher_tipo_pergunta.html"
    permission_required = ["questionarios.change_questionario"]

class PerguntaCreateView(PermissionRequiredMixin, CreateView):
    template_name = "questionarios/create_pergunta.html"
    model = Pergunta
    form_class = BasePerguntaForm
    permission_required = ["questionarios.change_questionario", "questionarios.add_pergunta"]
    pergunta_questionario = None
    
    def get_success_url(self):
        return reverse_lazy("questionarios:update_pergunta", kwargs = {"pk":self.pergunta_questionario.pk})

    def get_form_class(self):
        instance = self.kwargs.get("tipo")
        if instance == 0:
            return PerguntaEscolhaForm
        elif instance == 1:
            return PerguntaTextoForm
        elif instance == 2:
            return PerguntaArquivoForm
        elif instance == 3:
            return PerguntaImagemForm
        elif instance == 4:
            return PerguntaCoordenadaForm
        elif instance == 5:
            return PerguntaNumeroForm
        else:
            return None
    
    def get_form(self):
        form = super(PerguntaCreateView, self).get_form()
        questionario = get_object_or_404(Questionario, pk = self.kwargs.get("pk"))
        form.fields["pergunta_requisito"].queryset = Pergunta.objects.by_questionario(questionario)
        form.fields["possivel_escolha_requisito"].queryset = PossivelEscolha.by_questionario(questionario)
        return form

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        self.object = form.save()
        questionario = get_object_or_404(Questionario, pk = self.kwargs.get("pk"))
        self.pergunta_questionario = PerguntaDoQuestionario()
        self.pergunta_questionario.questionario = questionario
        self.pergunta_questionario.pergunta = self.object
        self.pergunta_questionario.save()
        return HttpResponseRedirect(self.get_success_url())

class PerguntaUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = "questionarios/update_pergunta.html"
    model = Pergunta
    form_class = BasePerguntaForm
    success_url = reverse_lazy("questionarios:list")
    permission_required = ["questionarios.change_questionario", "questionarios.change_pergunta"]
    pergunta_do_questionario = None

    def get_object(self):
        self.pergunta_do_questionario = get_object_or_404(PerguntaDoQuestionario, pk = self.kwargs.get("pk"))
        return self.pergunta_do_questionario.pergunta.cast()
    
    def get_form(self):
        form = super(PerguntaUpdateView, self).get_form()
        form.fields["pergunta_requisito"].queryset = Pergunta.objects.by_questionario(self.pergunta_do_questionario.questionario, self.object)
        form.fields["possivel_escolha_requisito"].queryset = PossivelEscolha.by_questionario(self.pergunta_do_questionario.questionario, exclude_pergunta=self.object)
        return form
    
    def get_context_data(self, **kwargs):
        context = super(PerguntaUpdateView, self).get_context_data(**kwargs)
        context["pergunta_do_questionario_pk"] = self.pergunta_do_questionario.pk
        return context

    def get_form_class(self):        

        if isinstance(self.object, PerguntaEscolha):
            return PerguntaEscolhaForm
        elif isinstance(self.object, PerguntaNumero):
            return PerguntaNumeroForm
        elif isinstance(self.object, PerguntaArquivo):
            return PerguntaArquivoForm
        elif isinstance(self.object, PerguntaTexto):
            return PerguntaTextoForm
        elif isinstance(self.object, PerguntaCoordenada):
            return PerguntaCoordenadaForm
        elif isinstance(self.object, PerguntaImagem):
            return PerguntaImagemForm
        else:
            return None


class PerguntaDoQuestionarioPerguntaRequisitoDeOutrosQuestionariosUpdateView(UpdateView):
    model = PerguntaDoQuestionario
    form_class = PerguntaRequisitoHiddenChangeForm
    template_name = "questionarios/update_pergunta_requisito.html"

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)

        questionario_pk = self.kwargs.get("questionario_pk", None)
        pergunta_questionario_pk = self.kwargs.get("pergunta_questionario_pk", None)

        if pergunta_questionario_pk is not None:
            pergunta_questionario = get_object_or_404(PerguntaDoQuestionario, pk = pergunta_questionario_pk)
            context["pergunta_questionario"] = pergunta_questionario

        elif questionario_pk is not None:
            questionario = get_object_or_404(Questionario, pk = questionario_pk)
            perguntas = PerguntaDoQuestionario.objects.filter(questionario = questionario).order_by("ordem")
            context["perguntas"] = perguntas

        else:
            questionarios = Questionario.objects.all().exclude(pk = self.object.questionario.pk)
            context["questionarios"] = questionarios
        
        return context
    


class PerguntaDoQuestionarioDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = "questionarios/delete_pergunta_do_questionario.html"
    model = PerguntaDoQuestionario
    success_url = reverse_lazy("questionarios:list")
    permission_required = ["questionarios.change_questionario", "questionarios.delete_perguntadoquestionario"]

"""PossivelEscolha"""

class PerguntaQuestionarioMixin(object):
    pergunta_do_questionario = None
    pergunta_do_questionario_pk_field = "pergunta_questionario_pk"

    def dispatch(self, request, *args, **kwargs):
        self.pergunta_do_questionario = get_object_or_404(PerguntaDoQuestionario, pk = self.kwargs.get(self.pergunta_do_questionario_pk_field))
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pergunta_do_questionario_pk"] = self.pergunta_do_questionario.pk
        return context

class PossivelEscolhaCreateView(PerguntaQuestionarioMixin, PermissionRequiredMixin, CreateView):
    template_name = "questionarios/create_possivelescolha.html"
    model = PossivelEscolha
    form_class = PossivelEscolhaForm
    permission_required = ["questionarios.change_questionario", "questionarios.change_pergunta", "questionarios.add_possivelescolha"]
    pergunta_do_questionario_pk_field = "pk"

    def form_valid(self, form):
        form.instance.pergunta = self.pergunta_do_questionario.pergunta.cast()
        return super(PossivelEscolhaCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy("questionarios:update_pergunta", kwargs = {"pk":self.kwargs.get("pk")})


class PossivelEscolhaUpdateView(PerguntaQuestionarioMixin, PermissionRequiredMixin, UpdateView):
    template_name = "questionarios/update_possivelescolha.html"
    model = PossivelEscolha
    form_class = PossivelEscolhaForm
    permission_required = ["questionarios.change_questionario", "questionarios.change_pergunta", "questionarios.change_possivelescolha"]
    pergunta_do_questionario_pk_field = "pergunta_questionario_pk"

    def get_success_url(self):
        return reverse_lazy("questionarios:update_pergunta", kwargs = {"pk":self.kwargs.get("pergunta_questionario_pk")})

class PossivelEscolhaDeleteView(PerguntaQuestionarioMixin, PermissionRequiredMixin, DeleteView):
    template_name = "questionarios/delete_possivelescolha.html"
    model = PossivelEscolha
    permission_required = ["questionarios.change_questionario", "questionarios.change_pergunta", "questionarios.delete_possivelescolha"]
    pergunta_do_questionario_pk_field = "pergunta_questionario_pk"

    def get_success_url(self):
        return reverse_lazy("questionarios:update_pergunta", kwargs = {"pk":self.kwargs.get("pergunta_questionario_pk")})


class TesteTemplateView(TemplateView):
    template_name = "questionarios/teste.html"


class PerguntaListView(PermissionRequiredMixin, ListView):
    model = Pergunta
    template_name = "questionarios/pergunta_list.html"
    permission_required = ["questionarios.view_pergunta", ]

    def get_queryset(self):
        return super(PerguntaListView, self).get_queryset().filter(usuario = self.request.user)