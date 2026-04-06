# File: map/views.py

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from establishments.models import Establishment


@login_required
def map_view(request):
    return render(request, 'map/map.html')


@login_required
def establishments_json(request):
    from django.utils import timezone
    from events.models import Event

    now = timezone.now()

    # Get all currently live events with their chat rooms
    live_events = Event.objects.filter(
        is_active=True,
        is_payment_verified=True,
        start_datetime__lte=now,
        end_datetime__gte=now,
    ).select_related('chat_room')

    # Map: establishment_id → chat_room_name (for the popup "Join Chat" button)
    est_chat_map = {}
    active_est_ids = set()
    for event in live_events:
        active_est_ids.add(event.establishment_id)
        if event.chat_room and event.chat_room.is_active:
            est_chat_map[event.establishment_id] = event.chat_room.room_name

    establishments = Establishment.objects.filter(
        is_verified=True,
        is_active=True,
        latitude__isnull=False,
        longitude__isnull=False,
    )

    data = []
    for est in establishments:
        has_live = est.id in active_est_ids
        data.append({
            'id':               est.id,
            'name':             est.name,
            'slug':             est.slug,
            'category':         est.get_category_display(),
            'category_key':     est.category,
            'city':             est.city,
            'latitude':         float(est.latitude),
            'longitude':        float(est.longitude),
            'has_active_event': has_live,
            # chat_room_name allows the popup "Join Chat" button to link directly
            # to /chat/{room_name}/ without any intermediate page load.
            'chat_room_name':   est_chat_map.get(est.id),
            'photo_url':        est.photo.url if est.photo else None,
        })

    return JsonResponse(data, safe=False)


@login_required
def establishment_detail(request, slug):
    """
    Returns the establishment detail partial HTML for the sidebar panel.
    The map JS fetches this via XHR and injects it into #sidebar-detail-content.
    It must NOT redirect or return a full page — just the partial template.
    """
    establishment = get_object_or_404(
        Establishment,
        slug=slug,
        is_verified=True,
        is_active=True,
    )
    # Render the partial — no base.html extension
    return render(request, 'map/establishment_detail.html', {
        'establishment': establishment,
    })