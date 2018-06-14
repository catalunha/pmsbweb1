from django.urls import path, include
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from rest_framework import routers, viewsets
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.authtoken.models import Token
from .serializers import QuestionarioSerializer, PerguntaSerializer, PossivelEscolhaSerializer, UserSerializer, User
from .models import Questionario, Pergunta, PossivelEscolha

class QuestionarioViewSet(viewsets.ModelViewSet):
    queryset = Questionario.objects.all()
    serializer_class = QuestionarioSerializer

class PerguntasViewSet(viewsets.ModelViewSet):
    queryset = Pergunta.objects.all()
    serializer_class = PerguntaSerializer

class PossivelEscolhaViewSet(viewsets.ModelViewSet):
    queryset = PossivelEscolha.objects.all()
    serializer_class = PossivelEscolhaSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

questionario_router = routers.DefaultRouter()
questionario_router.register(r'usuarios', UserViewSet)
questionario_router.register(r'questionarios', QuestionarioViewSet)
questionario_router.register(r'perguntas', PerguntasViewSet)
questionario_router.register(r'possiveis_escolhas', PossivelEscolhaViewSet)

urlpatterns = [
    path("get-auth-token", obtain_auth_token),
    path('', include(questionario_router.urls)),
]

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
