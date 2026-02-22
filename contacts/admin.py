from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'short_message', 'is_read', 'submitted_at']
    list_filter = ['is_read', 'submitted_at']
    search_fields = ['name', 'email', 'message']
    ordering = ['-submitted_at']
    list_editable = ['is_read']
    readonly_fields = ['name', 'email', 'message', 'submitted_at']

    def short_message(self, obj):
        return obj.message[:60] + '...' if len(obj.message) > 60 else obj.message
    short_message.short_description = 'Message'