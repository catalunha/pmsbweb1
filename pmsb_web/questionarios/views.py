from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View

from core.views import FakeDeleteView, FakeDeleteQuerysetViewMixin

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
    PerguntaRequisito,
    EscolhaRequisito,
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

    CreatePerguntaRequisitoForm,
    CreateEscolhaRequisitoForm,
)

from api.models import MobileApp

"""Questionario"""
class QuestionarioListView(PermissionRequiredMixin, FakeDeleteQuerysetViewMixin, ListView):
    model = Questionario
    template_name = "questionarios/list_questionario.html"
    permission_required = ["questionarios.view_questionario"]

    def get_queryset(self):
        equipe = self.request.GET.get('equipe', 'True')

        queryset = super(QuestionarioListView, self).get_queryset()
        queryset = queryset.filter(usuario = self.request.user)
        if equipe == 'True':
            superior_queryset = Questionario.objects.get_by_superior(
                usuario_superior=self.request.user,
            )

            queryset = superior_queryset | queryset

        return queryset.order_by('nome')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mobileapp'] = MobileApp.latest() or True
        return context


class QuestionarioEquipeListView(PermissionRequiredMixin, FakeDeleteQuerysetViewMixin, ListView):
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

class QuestioanrioUpdateView(PermissionRequiredMixin, FakeDeleteQuerysetViewMixin, UpdateView):
    template_name = "questionarios/update_questionario.html"
    model = Questionario
    form_class = QuestionarioForm
    permission_required = ["questionarios.change_questionario"]
    success_url = reverse_lazy("questionarios:list")

class QuestioanrioDeleteView(PermissionRequiredMixin, FakeDeleteQuerysetViewMixin, FakeDeleteView):
    template_name = "questionarios/delete_questionario.html"
    model = Questionario
    
    success_url = reverse_lazy("questionarios:list")
    permission_required = ["questionarios.delete_questionario"]

class QuestionarioOrdenarDetailView(PermissionRequiredMixin, FakeDeleteQuerysetViewMixin, DetailView):
    model = Questionario
    template_name = "questionarios/ordenar_detail.html"
    permission_required = ["questionarios.change_questionario"]

class QuestionarioOrdenarSubmitAjaxView(PermissionRequiredMixin, FakeDeleteQuerysetViewMixin, View):
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

class PerguntaUserPassTest(UserPassesTestMixin):
    """
    TODO: Testar implementação do teste de usuario permitido
    TODO: Adicionar teste as views
    """
    def test_func(self):
        pergunta = get_object_or_404(Pergunta, pk = self.kwargs.get(self.pk_url_kwarg))
        return self.request.user == pergunta.usuario or self.request.user.is_subordinado(pergunta.usuario)

class PerguntaEscolherTipoTemplateView(PermissionRequiredMixin, FakeDeleteQuerysetViewMixin, DetailView):
    model = Questionario
    template_name = "questionarios/escolher_tipo_pergunta.html"
    permission_required = ["questionarios.change_questionario"]

class PerguntaCreateView(PermissionRequiredMixin, CreateView):
    template_name = "questionarios/pergunta_create.html"
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

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        self.object = form.save()
        questionario = get_object_or_404(Questionario, pk = self.kwargs.get("pk"))
        self.pergunta_questionario = PerguntaDoQuestionario()
        self.pergunta_questionario.questionario = questionario
        self.pergunta_questionario.pergunta = self.object
        self.pergunta_questionario.save()
        return HttpResponseRedirect(self.get_success_url())

class PerguntaUpdateView(PermissionRequiredMixin, FakeDeleteQuerysetViewMixin, UpdateView):
    template_name = "questionarios/pergunta_update.html"
    model = Pergunta
    form_class = BasePerguntaForm
    success_url = reverse_lazy("questionarios:list")
    permission_required = ["questionarios.change_questionario", "questionarios.change_pergunta"]
    pergunta_do_questionario = None

    def get_object(self):
        self.pergunta_do_questionario = get_object_or_404(PerguntaDoQuestionario, pk = self.kwargs.get("pk"), fake_deletado = False)
        return self.pergunta_do_questionario.pergunta.cast()
    
    def get_context_data(self, **kwargs):
        context = super(PerguntaUpdateView, self).get_context_data(**kwargs)
        context['pergunta_do_questionario'] = self.pergunta_do_questionario        
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


"""Requisitos"""

class PerguntaDoQuestionarioPKOnContextMixin(object):
    pergunta_do_questionario_pk = None

    def get_context_data(self, **kwargs):
        assert self.pergunta_do_questionario_pk is not None, "pergunta_do_questionario_pk deve ser definida!" 
        context = super().get_context_data(**kwargs)
        context["pergunta_do_questionario_pk"] = self.kwargs.get(self.pergunta_do_questionario_pk)
        return context

class PerguntaRequisitoCreateView(PermissionRequiredMixin, PerguntaDoQuestionarioPKOnContextMixin, CreateView):
    template_name = "questionarios/perguntarequisito_create.html"
    model = PerguntaRequisito
    form_class = CreatePerguntaRequisitoForm
    permission_required = ["questionarios.change_questionario", "questionarios.change_pergunta"]
    pergunta_do_questionario_pk = "pk"

    def get_success_url(self):
        return reverse_lazy("questionarios:update_pergunta", kwargs = {"pk":self.kwargs.get("pk")})
    
    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        form = super().get_form()
        pergunta_do_questionario = get_object_or_404(PerguntaDoQuestionario, pk = self.kwargs.get("pk"))
        form.instance.pergunta = pergunta_do_questionario.pergunta
        return form

    def form_valid(self, form = None):
        return super().form_valid(form)

def ajax_get_perguntas_do_questionario(request):
    questionario_pk = request.GET.get("questionario_pk", None)
    perguntas_escolha = request.GET.get("perguntas_escolha", None)
    questionario_obj = get_object_or_404(Questionario, pk = questionario_pk, fake_deletado = False)
    
    queryset = questionario_obj.perguntas_do_questionario

    if perguntas_escolha == "True":
        queryset = queryset.filter(pergunta__tipo = PerguntaEscolha.TIPO)
    
    perguntas_do_questionario = queryset.values("id", "pergunta__variavel", "questionario__nome")

    rdict = dict()

    for p in perguntas_do_questionario:
        rdict[str(p["id"])] = {
            "id":p["id"],
            "pergunta":p["pergunta__variavel"],
            "questionario":p["questionario__nome"],
        }
    
    return JsonResponse(rdict)

def ajax_get_escolhas_da_pergunta_do_questionario(request):
    pergunta_do_questionario_pk = request.GET.get("pergunta_do_questionario_pk", None)
    pergunta_do_questionario_obj = get_object_or_404(PerguntaDoQuestionario, pk = pergunta_do_questionario_pk, fake_deletado = False)
    escolhas_da_pergunta_do_questionario = PossivelEscolha.objects.filter(
        pergunta = pergunta_do_questionario_obj.pergunta,
        fake_deletado = False).values("id", "texto")

    return JsonResponse(dict(escolhas=list(escolhas_da_pergunta_do_questionario)))


class PerguntaRequisitoDeleteView(PermissionRequiredMixin, PerguntaDoQuestionarioPKOnContextMixin, FakeDeleteQuerysetViewMixin, FakeDeleteView):
    model = PerguntaRequisito
    template_name = "questionarios/perguntarequisito_delete.html"
    permission_required = ["questionarios.change_questionario", "questionarios.change_pergunta"]
    pergunta_do_questionario_pk = "pergunta_do_questionario_pk"

    def get_success_url(self):
        return reverse_lazy("questionarios:update_pergunta", kwargs = {"pk":self.kwargs.get("pergunta_do_questionario_pk")})

class EscolhaRequisitoCreateView(PermissionRequiredMixin, PerguntaDoQuestionarioPKOnContextMixin, CreateView):
    template_name = "questionarios/escolharequisito_create.html"
    model = EscolhaRequisito
    form_class = CreateEscolhaRequisitoForm
    permission_required = ["questionarios.change_questionario", "questionarios.change_pergunta"]
    pergunta_do_questionario_pk = "pk"

    def get_success_url(self):
        return reverse_lazy("questionarios:update_pergunta", kwargs = {"pk":self.kwargs.get("pk")})
    
    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        form = super().get_form()
        pergunta_do_questionario = get_object_or_404(PerguntaDoQuestionario, pk = self.kwargs.get("pk"))
        form.instance.pergunta = pergunta_do_questionario.pergunta
        return form



class EscolhaRequisitoDeleteView(PermissionRequiredMixin, PerguntaDoQuestionarioPKOnContextMixin, FakeDeleteQuerysetViewMixin, FakeDeleteView):
    model = EscolhaRequisito
    template_name = "questionarios/escolharequisito_delete.html"
    permission_required = ["questionarios.change_questionario", "questionarios.change_pergunta"]
    pergunta_do_questionario_pk = "pergunta_do_questionario_pk"

    def get_success_url(self):
        return reverse_lazy("questionarios:update_pergunta", kwargs = {"pk":self.kwargs.get("pergunta_do_questionario_pk")})

class PerguntaDoQuestionarioDeleteView(PermissionRequiredMixin, FakeDeleteQuerysetViewMixin, FakeDeleteView):
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


class PossivelEscolhaUpdateView(PerguntaQuestionarioMixin, FakeDeleteQuerysetViewMixin, PermissionRequiredMixin, UpdateView):
    template_name = "questionarios/update_possivelescolha.html"
    model = PossivelEscolha
    form_class = PossivelEscolhaForm
    permission_required = ["questionarios.change_questionario", "questionarios.change_pergunta", "questionarios.change_possivelescolha"]
    pergunta_do_questionario_pk_field = "pergunta_questionario_pk"

    def get_success_url(self):
        return reverse_lazy("questionarios:update_pergunta", kwargs = {"pk":self.kwargs.get("pergunta_questionario_pk")})

class PossivelEscolhaDeleteView(PerguntaQuestionarioMixin, FakeDeleteQuerysetViewMixin, PermissionRequiredMixin, FakeDeleteView):
    template_name = "questionarios/delete_possivelescolha.html"
    model = PossivelEscolha
    permission_required = ["questionarios.change_questionario", "questionarios.change_pergunta", "questionarios.delete_possivelescolha"]
    pergunta_do_questionario_pk_field = "pergunta_questionario_pk"

    def get_success_url(self):
        return reverse_lazy("questionarios:update_pergunta", kwargs = {"pk":self.kwargs.get("pergunta_questionario_pk")})


class TesteTemplateView(TemplateView):
    template_name = "questionarios/teste.html"


class PerguntaListView(PermissionRequiredMixin, FakeDeleteQuerysetViewMixin, ListView):
    model = Pergunta
    template_name = "questionarios/pergunta_list.html"
    permission_required = ["questionarios.view_pergunta", ]

    def get_queryset(self):
        return super(PerguntaListView, self).get_queryset().filter(usuario = self.request.user)

class PerguntaDetailView(PermissionRequiredMixin, DetailView):
    model = Pergunta
    template_name = "questionarios/pergunta_detail.html"
    permission_required = ["questionarios.view_pergunta", ]