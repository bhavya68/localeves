# File: events/views.py

import hmac
import hashlib

import razorpay
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, Http404
from django.conf import settings

from establishments.models import Establishment
from chat.models import ChatRoom
from .models import Event


def _razorpay_client():
    return razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )


def _activate_event(event, payment_id='mock'):
    """Mark event as verified and create its chat room."""
    event.razorpay_payment_id = payment_id
    event.is_payment_verified = True
    event.save(update_fields=['razorpay_payment_id', 'is_payment_verified'])

    room = ChatRoom.objects.create(
        establishment=event.establishment,
        room_name=f'event_{event.id}',
        is_active=True,
    )
    event.chat_room = room
    event.save(update_fields=['chat_room'])


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

        if settings.DEBUG:
            # In dev, skip Razorpay order creation — use a placeholder
            razorpay_order_id = 'dev_mock_order'
        else:
            client = _razorpay_client()
            rz_order = client.order.create({
                'amount': settings.EVENT_PRICE_PAISE,
                'currency': 'INR',
                'payment_capture': 1,
            })
            razorpay_order_id = rz_order['id']

        event = Event.objects.create(
            establishment=establishment,
            created_by=request.user,
            name=name,
            description=description,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            razorpay_order_id=razorpay_order_id,
            amount_paid=settings.EVENT_PRICE_PAISE,
            is_payment_verified=False,
        )

        return redirect('events:review_event', event_id=event.id)

    return render(request, 'events/create_event.html', {
        'establishment': establishment,
        'price': settings.EVENT_PRICE_PAISE // 100,
    })


@login_required
def review_event(request, event_id):
    event = get_object_or_404(
        Event,
        id=event_id,
        created_by=request.user,
        is_payment_verified=False,
    )

    return render(request, 'events/review_event.html', {
        'event': event,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'amount_paise': settings.EVENT_PRICE_PAISE,
        'amount_rupees': settings.EVENT_PRICE_PAISE // 100,
        'debug': settings.DEBUG,
    })


@login_required
def mock_payment_success(request, event_id):
    """
    Dev-only endpoint. Simulates a successful payment without hitting Razorpay.
    Raises 404 in production so it can never be abused.
    """
    if not settings.DEBUG:
        raise Http404

    if request.method != 'POST':
        return HttpResponseBadRequest('POST required')

    event = get_object_or_404(
        Event,
        id=event_id,
        created_by=request.user,
        is_payment_verified=False,
    )

    _activate_event(event, payment_id='mock_dev_payment')
    messages.success(request, f'🎉 Event "{event.name}" is now live! (simulated payment)')
    return redirect('establishments:dashboard')


@login_required
def cancel_event(request, event_id):
    """Delete a pending (unpaid) event."""
    event = get_object_or_404(
        Event,
        id=event_id,
        created_by=request.user,
        is_payment_verified=False,
    )
    event.delete()
    messages.info(request, 'Event creation cancelled.')
    return redirect('establishments:dashboard')


@csrf_exempt
def payment_success(request):
    """
    Production only. Razorpay POSTs here after real payment.
    Verifies the HMAC signature before trusting anything.
    """
    if request.method != 'POST':
        return HttpResponseBadRequest('POST required')

    payment_id = request.POST.get('razorpay_payment_id', '')
    order_id   = request.POST.get('razorpay_order_id', '')
    signature  = request.POST.get('razorpay_signature', '')

    body = f'{order_id}|{payment_id}'
    expected = hmac.new(
        settings.RAZORPAY_KEY_SECRET.encode(),
        body.encode(),
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(expected, signature):
        messages.error(request, 'Payment verification failed. Please contact support.')
        return redirect('establishments:dashboard')

    try:
        event = Event.objects.get(
            razorpay_order_id=order_id,
            is_payment_verified=False,
        )
    except Event.DoesNotExist:
        messages.error(request, 'No matching event found for this payment.')
        return redirect('establishments:dashboard')

    _activate_event(event, payment_id=payment_id)
    messages.success(request, f'🎉 Event "{event.name}" is now live!')
    return redirect('establishments:dashboard')