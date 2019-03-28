from django.urls import path
from rest_framework_swagger.views import get_swagger_view

urlpatterns = [
    path('swagger', get_swagger_view(title="PMSB API")),
]
