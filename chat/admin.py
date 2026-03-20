# File: chat/admin.py

from django.contrib import admin
from .models import ChatRoom, Message


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['room_name', 'establishment', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['room_name', 'establishment__name']
    readonly_fields = ['created_at']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'room', 'content_preview', 'timestamp']
    list_filter = ['room', 'timestamp']
    search_fields = ['user__email', 'content']
    readonly_fields = ['timestamp']

    def content_preview(self, obj):
        return obj.content[:60]

    content_preview.short_description = 'Content'