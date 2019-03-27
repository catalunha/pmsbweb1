from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

urlpatterns = [
    path('pmsb/', include(('conta.urls', 'conta'), namespace='conta')),
    path('pmsb/admin/', admin.site.urls),
    path('pmsb/api/', include("api.urls")),
    path('pmsb/tarefas/', include('pinax.messages.urls', namespace='pinax_messages')),
    path("pmsb/questionarios/", include("questionarios.urls")),
    path("pmsb/relatorios/", include("relatorios.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path('pmsb/docs/api/swagger', get_swagger_view(title="PMSB API")),
    ]
