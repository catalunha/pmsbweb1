from django.urls import path, include
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from rest_framework import routers, viewsets
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.authtoken.models import Token
from .serializers import UserViewSet, QuestionarioViewSet, PerguntasViewSet, PossivelEscolhaViewSet, RespostaQuestionarioViewSet, RespostaPerguntaViewSet

questionario_router = routers.DefaultRouter()
questionario_router.register(r'usuarios', UserViewSet)
questionario_router.register(r'questionarios', QuestionarioViewSet)
questionario_router.register(r'perguntas', PerguntasViewSet)
questionario_router.register(r'possiveis_escolhas', PossivelEscolhaViewSet)
questionario_router.register(r'resposta', RespostaQuestionarioViewSet)
questionario_router.register(r'resposta_pergunta', RespostaPerguntaViewSet)

urlpatterns = [
    path("get-auth-token", obtain_auth_token),
    path('', include(questionario_router.urls)),
]

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
