from django.shortcuts import render, get_object_or_404
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
from django.views.generic.edit import FormMixin, ProcessFormView
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
)


class QuestionarioListView(PermissionRequiredMixin, ListView):
    model = Questionario
    template_name = "questionarios/list_questionario.html"
    permission_required = ["questionarios.view_questionario"]

    def get_queryset(self):
        queryset = super(QuestionarioListView, self).get_queryset()
        return queryset.filter(usuario = self.request.user)

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

class QuestionarioOrdenarView(View):
    pass 
    
class PerguntaEscolherTipoTemplateView(PermissionRequiredMixin, DetailView):
    model = Questionario
    template_name = "questionarios/escolher_tipo_pergunta.html"
    permission_required = ["questionarios.change_questionario"]

class PerguntaCreateView(PermissionRequiredMixin, CreateView):
    template_name = "questionarios/create_pergunta.html"
    model = Pergunta
    form_class = BasePerguntaForm
    permission_required = ["questionarios.change_questionario", "questionarios.add_pergunta"]
    
    def get_success_url(self):
        return reverse_lazy("questionarios:update_pergunta", kwargs = {"pk":self.object.pk, "questionario_pk":self.kwargs.get("pk")})

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
        form.fields["possivel_escolha_requisito"].queryset = PossivelEscolha.by_id_questionario(self.kwargs.get("pk"))
        return form

    def form_valid(self, form):
        form_valid_return = super(PerguntaCreateView, self).form_valid(form)
        
        questionario = get_object_or_404(Questionario, pk = self.kwargs.get("pk"))
        pergunta_questionario = PerguntaDoQuestionario()
        pergunta_questionario.questionario = questionario
        pergunta_questionario.pergunta = self.object
        pergunta_questionario.save()

        return form_valid_return

class PerguntaUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = "questionarios/update_pergunta.html"
    model = Pergunta
    form_class = BasePerguntaForm
    success_url = reverse_lazy("questionarios:list")
    permission_required = ["questionarios.change_questionario", "questionarios.change_pergunta"]

    def get_object(self):
        self.object = super(PerguntaUpdateView, self).get_object()
        self.object = self.object.cast()
        return self.object

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

class PerguntaDoQuestionarioDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = "questionarios/delete_pergunta_do_questionario.html"
    model = PerguntaDoQuestionario
    success_url = reverse_lazy("questionarios:list")
    permission_required = ["questionarios.change_questionario", "questionarios.delete_pergunta", "questionarios.delete_perguntadoquestionario"]


class TesteTemplateView(TemplateView):
    template_name = "questionarios/teste.html"
