from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

from .signals import message_sent
from .utils import cached_attribute

from core.mixins import TimedModelMixin, UUIDModelMixin, UserOwnedModelMixin, FakeDeleteModelMixin

@python_2_unicode_compatible
class Thread(UUIDModelMixin, TimedModelMixin, FakeDeleteModelMixin):

    subject = models.CharField("Título da Tarefa", max_length=150)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through="UserThread")
    data_de_entrega = models.DateField("Prazo", null=True, blank=True)
    data_finalizada = models.DateField("Finalizada em", null=True, blank=True)

    @classmethod
    def inbox(cls, user):
        return cls.objects.filter(userthread__user=user, userthread__deleted=False, fake_deletado=False)

    @classmethod
    def deleted(cls, user):
        return cls.objects.filter(userthread__user=user, userthread__deleted=True, fake_deletado=False)

    @classmethod
    def unread(cls, user):
        return cls.objects.filter(userthread__user=user, userthread__deleted=False, fake_deletado=False)

    def __str__(self):
        return "{}: {} Prazo: {}".format(
            self.subject,
            ", ".join([str(user) for user in self.users.all()]), self.data_de_entrega
        )

    def get_absolute_url(self):
        return reverse("pinax_messages:thread_detail", args=[self.pk])

    @property
    @cached_attribute
    def first_message(self):
        return self.messages.order_by("sent_at")[0]

    @property
    @cached_attribute
    def latest_message(self):
        return self.messages.all()[0]

    @classmethod
    def ordered(cls, objs):
        """
        Returns the iterable ordered the correct way, this is a class method
        because we don"t know what the type of the iterable will be.
        """
        objs = list(objs)
        objs.sort(key=lambda o: o.latest_message.sent_at, reverse=True)
        return objs


class UserThread(UUIDModelMixin, TimedModelMixin, FakeDeleteModelMixin):

    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    unread = models.BooleanField()
    deleted = models.BooleanField()

def documento_upload(instance, filename):
    """
    media/<id_thread>/<id_user>/<nome_do_arquivo>
    """
    return 'upload/{0}/{1}/{0}_{2}'.format(instance.thread.id, instance.sender.id, filename)

class Message(UUIDModelMixin, TimedModelMixin, FakeDeleteModelMixin):

    thread = models.ForeignKey(Thread, related_name="messages", on_delete=models.CASCADE)

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="sent_messages", on_delete=models.CASCADE)
    sent_at = models.DateTimeField(default=timezone.now)

    content = models.TextField()

    file_upload = models.FileField(upload_to=documento_upload, null=True, blank=True)

    @classmethod
    def new_reply(cls, thread, user, content, arquivo):
        """
        Create a new reply for an existing Thread.
        Mark thread as unread for all other participants, and
        mark thread as read by replier.
        """
        msg = cls.objects.create(thread=thread, sender=user, content=content, file_upload=arquivo)
        thread.userthread_set.exclude(user=user).update(unread=True)
        thread.userthread_set.filter(user=user).update(unread=False)
        message_sent.send(sender=cls, message=msg, thread=thread, reply=True)
        return msg

    @classmethod
    def new_message(cls, from_user, to_users, subject, content, data_de_entrega, arquivo):
        """
        Create a new Message and Thread.
        Mark thread as unread for all recipients, and
        mark thread as read and deleted from inbox by creator.
        """
        thread = Thread.objects.create(subject=subject, data_de_entrega=data_de_entrega)
        for user in to_users:
            thread.userthread_set.create(user=user, deleted=False, unread=False)
        thread.userthread_set.create(user=from_user, deleted=False, unread=False)
        msg = cls.objects.create(thread=thread, sender=from_user, content=content, file_upload=arquivo)
        message_sent.send(sender=cls, message=msg, thread=thread, reply=False)
        return msg

    class Meta:
        ordering = ("-sent_at",)

    def get_absolute_url(self):
        return self.thread.get_absolute_url()