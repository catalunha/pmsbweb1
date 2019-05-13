from django.db import models
from django.apps import apps

def app_choices():
    c = []
    for app in apps.get_app_configs():
        c.append((app.name, app.name))
    return c


class AppBlock(models.Model):
    app_name = models.CharField(max_length=255, choices=app_choices(), unique=True)

    def __str__(self):
        return self.app_name