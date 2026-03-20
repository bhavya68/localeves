# File: chat/models.py

import uuid
from django.db import models
from django.conf import settings
from establishments.models import Establishment


class ChatRoom(models.Model):

    establishment = models.ForeignKey(
        Establishment,
        on_delete=models.CASCADE,
        related_name='chat_rooms',
       
    )

    room_name = models.CharField(
        max_length=100,
        unique=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Chat Room'
        verbose_name_plural = 'Chat Rooms'
        ordering = ['-created_at']

    def __str__(self):
        return f'Room: {self.room_name} ({self.establishment.name})'


class Message(models.Model):

    room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name='messages',
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='chat_messages',
    )

    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['timestamp']

    def __str__(self):
        username = self.user.username if self.user else 'Deleted User'
        return f'{username} in {self.room.room_name}: {self.content[:40]}'