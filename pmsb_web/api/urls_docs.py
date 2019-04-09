from django.contrib.auth.decorators import (login_required, user_passes_test)
from django.urls import path
from rest_framework_swagger.views import get_swagger_view


def user_is_staff(user):
    return user.is_staff


login_required_docs = login_required(get_swagger_view(title="PMSB API"))

docs = user_passes_test(test_func=user_is_staff)(login_required_docs)

urlpatterns = [
    path('swagger', docs),
]
