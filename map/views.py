
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from establishments.models import Establishment

@login_required
def map_view(request):
    return render(request, 'map/map.html')

@login_required
def establishments_json(request):
   
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
            'has_active_event': False,
           
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