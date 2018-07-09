from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView
# Create your views here.

class ListarQuestionarios(ListView):
    pass

class CriarQuesqionario(CreateView):
    pass

class EditarQuestioanrio(UpdateView):
    pass