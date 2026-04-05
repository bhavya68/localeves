# File: events/urls.py

from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('create/<slug:establishment_slug>/', views.create_event,        name='create_event'),
    path('review/<int:event_id>/',            views.review_event,         name='review_event'),
    path('cancel/<int:event_id>/',            views.cancel_event,         name='cancel_event'),
    path('mock-success/<int:event_id>/',      views.mock_payment_success, name='mock_payment_success'),
    path('payment-success/',                  views.payment_success,      name='payment_success'),
    path('<int:event_id>/',                   views.event_detail,         name='event_detail'),
]