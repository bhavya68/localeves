
from django.urls import path
from . import views

app_name = 'map'

urlpatterns = [
    path('', views.map_view, name='map_view'),
    path('establishments.json', views.establishments_json, name='establishments_json'),

    path('establishment/<slug:slug>/', views.establishment_detail, name='establishment_detail'),
]