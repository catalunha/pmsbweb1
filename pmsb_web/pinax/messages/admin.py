from django.contrib import admin

from .models import Message, UserThread, Thread


class UserThreadAdmin(admin.ModelAdmin):
    list_display = ["id","thread", "user", "unread", "deleted"]
    list_filter = ["unread", "deleted"]
    raw_id_fields = ["user"]

class ThreadAdmin(admin.ModelAdmin):
    list_display = ["id","subject"]


class MessageAdmin(admin.ModelAdmin):
    list_display = ["id","thread", "sender", "sent_at"]
    list_filter = ["sent_at", "thread"]
    raw_id_fields = ["sender"]


admin.site.register(Message, MessageAdmin)
admin.site.register(UserThread, UserThreadAdmin)
admin.site.register(Thread, ThreadAdmin)
