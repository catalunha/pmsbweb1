from django.contrib import admin

from api.models import MobileApp

class MobileAppAdmin(admin.ModelAdmin):
    list_display = ('pk','major', 'minor', 'patch')
    list_filter = ('major', 'minor')

admin.site.register(MobileApp, MobileAppAdmin)
