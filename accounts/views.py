from django.shortcuts import render
from django.utils import timezone
from events.models import Event


def home(request):
    from django.utils import timezone
    from events.models import Event
    from establishments.models import Establishment

    now = timezone.now()

    live_count = Event.objects.filter(
        is_active=True,
        is_payment_verified=True,
        start_datetime__lte=now,
        end_datetime__gte=now,
    ).count()

    upcoming_count = Event.objects.filter(
        is_active=True,
        is_payment_verified=True,
        start_datetime__gt=now,
    ).count()

    establishment_count = Establishment.objects.filter(
        is_verified=True,
        is_active=True,
    ).count()

    return render(request, 'home.html', {
        'live_count': live_count,
        'upcoming_count': upcoming_count,
        'establishment_count': establishment_count,
    })