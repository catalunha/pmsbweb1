from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView, TemplateView

from .models import Questionario, Pergunta, PerguntaDoQuestionario

class ListarQuestionarios(ListView):
    model = Questionario
    template_name = "questionarios/listar.html"

class CriarQuesqionario(CreateView):
    template_name = "questionarios/criar.html"
    success_url = reverse_lazy("questionarios:editar")

class EditarQuestioanrio(UpdateView):
    template_name = "questionarios/editar.html"

class AdicionaPerguntaView(CreateView):
    model = Pergunta
    template_name = "questionarios/adicionar_pergunta.html"

class TesteView(TemplateView):
    template_name = "questionarios/listar_questionarios.html"