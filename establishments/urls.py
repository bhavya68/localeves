
from django.urls import path
from . import views

app_name = 'establishments'

urlpatterns = [
    path('register/', views.owner_register, name='register'),


    path('verify-otp/', views.verify_otp, name='verify_otp'),


    path('dashboard/', views.owner_dashboard, name='dashboard'),
]