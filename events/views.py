# File: events/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from establishments.models import Establishment
from chat.models import ChatRoom
from .models import Event


@login_required
def create_event(request, establishment_slug):
    establishment = get_object_or_404(
        Establishment,
        slug=establishment_slug,
        owner=request.user,
        is_verified=True,
    )

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        start_datetime = request.POST.get('start_datetime', '').strip()
        end_datetime = request.POST.get('end_datetime', '').strip()

        errors = []
        if not name:
            errors.append('Event name is required.')
        if not start_datetime or not end_datetime:
            errors.append('Start and end times are required.')

        if errors:
            return render(request, 'events/create_event.html', {
                'establishment': establishment,
                'errors': errors,
                'price': settings.EVENT_PRICE_PAISE // 100,
            })

        event = Event.objects.create(
            establishment=establishment,
            created_by=request.user,
            name=name,
            description=description,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            razorpay_order_id='mock_order',
            amount_paid=settings.EVENT_PRICE_PAISE,
            is_payment_verified=True,
        )

        room = ChatRoom.objects.create(
            establishment=establishment,
            room_name=f'event_{event.id}',
            is_active=True,
        )
        event.chat_room = room
        event.save()

        messages.success(request, f'Event "{name}" created successfully!')
        return redirect('establishments:dashboard')

    return render(request, 'events/create_event.html', {
        'establishment': establishment,
        'price': settings.EVENT_PRICE_PAISE // 100,
    })