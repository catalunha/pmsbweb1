from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, TemplateView
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
)
from .forms import (
    QuestionarioForm,
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

class QuestionarioCreateView(LoginRequiredMixin, CreateView):
    model = Questionario
    form_class = QuestionarioForm
    template_name = "questionarios/create_questionario.html"
    success_url = reverse_lazy("questionarios:list")

class QuestioanrioUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "questionarios/update_questionario.html"
    model = Questionario
    form_class = QuestionarioForm
    success_url = reverse_lazy("questionarios:list")

class QuestionarioOrdenarView(View):
    pass 

class QuestioanrioDeleteView(DeleteView):
    template_name = "questionarios/delete_questionario.html"
    model = Questionario
    success_url = reverse_lazy("questionarios:list")

class PerguntaEscolherTipoTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "questionarios/escolher_tipo_pergunta.html"

class PerguntaCreateView(LoginRequiredMixin, CreateView):
    model = Pergunta
    template_name = "questionarios/create_pergunta.html"

class PerguntaUpdateView(LoginRequiredMixin, UpdateView):
    model = Pergunta
    template_name = "questionarios/update_pergunta.html"

    def get_form_class(self):
        
        instance = self.object.cast()

        if isinstance(instance, PerguntaEscolha):
            return PerguntaEscolhaForm
        elif isinstance(instance, PerguntaNumero):
            return PerguntaNumeroForm
        elif isinstance(instance, PerguntaArquivo):
            return PerguntaArquivoForm
        elif isinstance(instance, PerguntaTexto):
            return PerguntaTextoForm
        elif isinstance(instance, PerguntaCoordenada):
            return PerguntaCoordenadaForm
        elif isinstance(instance, PerguntaImagem):
            return PerguntaImagemForm
        else:
            return None

class PerguntaDeleteView(DeleteView):
    pass