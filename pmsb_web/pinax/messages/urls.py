from django.conf.urls import url
from django.urls import path

from . import views

app_name = "pinax_messages"

urlpatterns = [
    path('inbox/', views.InboxView.as_view(),
        name="inbox"),
    url(r"^create/$", views.MessageCreateView.as_view(),
        name="message_create"),
    url(r"^create/(?P<user_id>\d+)/$", views.MessageCreateView.as_view(),
        name="message_user_create"),
    url(r"^thread/(?P<pk>[\w-]+)/$", views.ThreadView.as_view(),
        name="thread_detail"),
    url(r"^thread/(?P<pk>[\w-]+)/delete/$", views.ThreadDeleteView.as_view(),
        name="thread_delete"),
]
