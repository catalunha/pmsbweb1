from django.urls import path, include
from rest_framework import routers, viewsets
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

print("possivel escolha serielizer asdf asdfnla ",UserSerializer())
print("possivel escolha serielizer asdf asdfnla ",QuestionarioSerializer())
print("possivel escolha serielizer asdf asdfnla ",PerguntaSerializer())
print("possivel escolha serielizer asdf asdfnla ",PossivelEscolhaSerializer())

questionario_router = routers.DefaultRouter()
questionario_router.register(r'usuarios', UserViewSet)
questionario_router.register(r'questionarios', QuestionarioViewSet)
questionario_router.register(r'perguntas', PerguntasViewSet)
questionario_router.register(r'possiveis_escolhas', PossivelEscolhaViewSet)

urlpatterns = [
    path('', include(questionario_router.urls)),
]