from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView, TemplateView
# Create your views here.

class ListarQuestionarios(ListView):
    pass

class CriarQuesqionario(CreateView):
    pass

class EditarQuestioanrio(UpdateView):
    pass

class TesteView(TemplateView):
    template_name = "questionarios/listar_questionarios.html"