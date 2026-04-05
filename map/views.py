
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

    active_event_establishment_ids = set(
        Event.objects.filter(
            is_active=True,
            is_payment_verified=True,
            start_datetime__lte=now,
            end_datetime__gte=now,
        ).values_list('establishment_id', flat=True)
    )

    establishments = Establishment.objects.filter(
        is_verified=True,
        is_active=True,
        latitude__isnull=False,
        longitude__isnull=False,
    ).select_related('owner')

    data = []
    for est in establishments:
        data.append({
            'id': est.id,
            'name': est.name,
            'slug': est.slug,
            'category': est.get_category_display(),
            'city': est.city,
            'latitude': float(est.latitude),
            'longitude': float(est.longitude),
            'has_active_event': est.id in active_event_establishment_ids,
        })

    return JsonResponse(data, safe=False)

@login_required
def establishment_detail(request, slug):
    
    establishment = get_object_or_404(
        Establishment,
        slug=slug,
        is_verified=True,
        is_active=True,
    )

    return render(request, 'map/establishment_detail.html', {
        'establishment': establishment,
    })