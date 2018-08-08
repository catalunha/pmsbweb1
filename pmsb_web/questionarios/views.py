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
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

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


class QuestionarioListView(LoginRequiredMixin, ListView):
    model = Questionario
    template_name = "questionarios/list_questionario.html"

    def get_queryset(self):
        queryset = super(QuestionarioListView, self).get_queryset()
        return queryset.filter(usuario = self.request.user)

class QuestionarioCreateView(LoginRequiredMixin, CreateView):
    model = Questionario
    form_class = QuestionarioForm
    template_name = "questionarios/create_questionario.html"
    success_url = reverse_lazy("questionarios:list")

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super(QuestionarioCreateView, self).form_valid(form)

class QuestioanrioUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "questionarios/update_questionario.html"
    model = Questionario
    form_class = QuestionarioForm
    success_url = reverse_lazy("questionarios:list")

class QuestionarioOrdenarView(View):
    pass 

class QuestioanrioDeleteView(FormMixin, DeleteView):
    template_name = "questionarios/delete_questionario.html"
    model = Questionario
    form_class = QuestionarioDeleteForm
    success_url = reverse_lazy("questionarios:list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        form.object_id = self.kwargs.get("pk")
        if form.is_valid():
            return super(QuestioanrioDeleteView, self).post(request, *args, **kwargs)
        else:
            return self.form_invalid(form)



    
class PerguntaEscolherTipoTemplateView(LoginRequiredMixin, DetailView):
    model = Questionario
    template_name = "questionarios/escolher_tipo_pergunta.html"

class PerguntaCreateView(LoginRequiredMixin, CreateView):
    template_name = "questionarios/create_pergunta.html"
    model = Pergunta
    form_class = BasePerguntaForm
    
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

class PerguntaUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "questionarios/update_pergunta.html"
    model = Pergunta
    form_class = BasePerguntaForm
    success_url = reverse_lazy("questionarios:list")

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

class PerguntaDoQuestionarioDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "questionarios/delete_pergunta_do_questionario.html"
    model = PerguntaDoQuestionario
    success_url = reverse_lazy("questionarios:list")


class TesteTemplateView(TemplateView):
    template_name = "questionarios/teste.html"
