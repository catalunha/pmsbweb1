from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include(('conta.urls', 'conta'), namespace='conta')),
    path('tarefas/', include('pinax.messages.urls', namespace='pinax_messages')),
    path('questionarios/', include("questionarios.urls")),
    path('relatorios/', include("relatorios.urls")),

    path('admin/', admin.site.urls),
    path('api/', include("api.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
