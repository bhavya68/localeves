# File: events/urls.py

from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('create/<slug:establishment_slug>/', views.create_event, name='create_event'),
]