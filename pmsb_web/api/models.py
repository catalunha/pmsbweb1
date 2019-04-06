from django.db import models
from core.mixins import TimedModelMixin, UUIDModelMixin

MEDIA_ROOT = 'api'
MOBILE_APP_MEDIA_ROOT = 'mobile'

def android_upload_to(instance, filename):
    return f"{MEDIA_ROOT}/{MOBILE_APP_MEDIA_ROOT}/{instance.pk}.apk"

def ios_upload_to(instance, filename):
    return f"{MEDIA_ROOT}/{MOBILE_APP_MEDIA_ROOT}/{instance.pk}.ipa"

class MobileApp(UUIDModelMixin, TimedModelMixin):
    android = models.FileField(upload_to=android_upload_to, null=True, blank=True)
    ios = models.FileField(upload_to=ios_upload_to, null=True, blank=True)
    major = models.SmallIntegerField()
    minor = models.SmallIntegerField()
    patch = models.SmallIntegerField()
    liberado = models.BooleanField(default=False)
    descricao = models.TextField()

    class Meta:
        ordering = ('-major', '-minor', '-patch')

    def __str__(self):
        return self.versao()
    

    def versao(self):
        return f"{self.major}.{self.minor}.{self.patch}"
    

    @classmethod
    def latest(cls):
        return cls.objects.filter(liberado=True).first()

