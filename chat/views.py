# File: chat/views.py

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ChatRoom


@login_required
def chat_room(request, room_name):
  
    room = get_object_or_404(
        ChatRoom,
        room_name=room_name,
        is_active=True,
    )

    return render(request, 'chat/chat_room.html', {
        'room': room,
       
    })