from django import forms
from django.contrib import admin
from .models import AppBlock

admin.site.site_header = "PMSB"
admin.site.site_title = "PMSB"

# visualização de log do djangoAdmin
admin.site.register(admin.models.LogEntry)


class AppBlockAdmin(admin.ModelAdmin):
    list_display = ("id", "app_name")


admin.site.register(AppBlock, AppBlockAdmin)
