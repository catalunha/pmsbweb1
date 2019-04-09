from django.urls import path, include
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from rest_framework import routers, viewsets
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.authtoken.models import Token

from .serializers import (
    LocalizacaoViewSet,
    UserViewSet,
    QuestionarioViewSet,
    PossivelEscolhaViewSet,
    RespostaQuestionarioViewSet,
    RespostaPerguntaViewSet,
    PerguntasViewSet,
    PerguntaEscolhaViewSet,
    PerguntaNumeroViewSet,
    PerguntaArquivoViewSet,
    PerguntaImagemViewSet,
    PerguntaTextoViewSet,
    PerguntaCoordenadaViewSet,

    PossivelEscolhaRespostaViewSet,
    CoordenadaRespostaViewSet,
    TextoRespostaViewSet,
    NumeroRespostaViewSet,
    ArquivoRespostaViewSet,
    ImagemRespostaViewSet,

    PerguntaRequisitoViewSet,
    EscolhaRequisitoViewSet,

    SetorCensitarioViewset,
    SetorCensitarioExpandidoViewset,
)

questionario_router = routers.DefaultRouter()

questionario_router.register(r'localizacoes', LocalizacaoViewSet)

questionario_router.register(r'usuarios', UserViewSet)

questionario_router.register(r'questionarios', QuestionarioViewSet)
questionario_router.register(r'perguntas', PerguntasViewSet)
questionario_router.register(r'perguntas_escolha', PerguntaEscolhaViewSet)
questionario_router.register(r'perguntas_numero', PerguntaNumeroViewSet)
questionario_router.register(r'perguntas_arquivo', PerguntaArquivoViewSet)
questionario_router.register(r'perguntas_imagem', PerguntaImagemViewSet)
questionario_router.register(r'perguntas_texto', PerguntaTextoViewSet)
questionario_router.register(r'perguntas_coordenada', PerguntaCoordenadaViewSet)
questionario_router.register(r'perguntas', PerguntasViewSet)
questionario_router.register(r'possiveis_escolhas', PossivelEscolhaViewSet)

questionario_router.register(r'respostas', RespostaQuestionarioViewSet)
questionario_router.register(r'respostas_pergunta', RespostaPerguntaViewSet)


questionario_router.register(r'possivel_escolhas_respostas', PossivelEscolhaRespostaViewSet)
questionario_router.register(r'coordenada_respostas', CoordenadaRespostaViewSet)
questionario_router.register(r'texto_respostas', TextoRespostaViewSet)
questionario_router.register(r'numero_respostas', NumeroRespostaViewSet)
questionario_router.register(r'arquivo_respostas', ArquivoRespostaViewSet)
questionario_router.register(r'imagem_respostas', ImagemRespostaViewSet)

questionario_router.register(r'perguntas_requisito', PerguntaRequisitoViewSet)
questionario_router.register(r'escolhas_requisito', EscolhaRequisitoViewSet)

questionario_router.register(r'setores_censitarios', SetorCensitarioViewset)
questionario_router.register(r'setores_censitarios_expandido', SetorCensitarioExpandidoViewset)
urlpatterns = [
    path("get-auth-token", obtain_auth_token),
    path('', include(questionario_router.urls)),
]

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
