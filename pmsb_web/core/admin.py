from django.contrib import admin

admin.site.site_header = "PMSB"
admin.site.site_title = "PMSB"

#visualização de log do djangoAdmin
admin.site.register(admin.models.LogEntry)