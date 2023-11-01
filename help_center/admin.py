from django.contrib import admin
from .models import ContactMessage, LiveChatMessage

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'message')
    search_fields = ('name', 'email', 'subject', 'message')
    list_filter = ('subject',)

class LiveChatMessageAdmin(admin.ModelAdmin):
    list_display = ('sender_name', 'message', 'timestamp')
    search_fields = ('sender_name', 'message')
    list_filter = ('timestamp',)

# Register the models and associated admin classes
admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(LiveChatMessage, LiveChatMessageAdmin)