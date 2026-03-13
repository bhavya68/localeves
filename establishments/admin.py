
from django.contrib import admin
from .models import Establishment, OwnerOTP


@admin.register(Establishment)
class EstablishmentAdmin(admin.ModelAdmin):

    list_display = [
        'name',
        'owner',
        'category',
        'city',
        'is_verified',
        'is_active',
        'created_at',
    ]

    list_filter = ['category', 'is_verified', 'is_active', 'city']
    search_fields = ['name', 'owner__email', 'city', 'address']
  
    readonly_fields = ['slug', 'created_at', 'updated_at']

    fieldsets = (
        ('Basic Details', {
            'fields': ('owner', 'name', 'slug', 'category', 'description')
        }),
        ('Location', {
            'fields': ('address', 'city', 'latitude', 'longitude')
        }),
        ('Contact & Media', {
            'fields': ('contact_phone', 'contact_email', 'photo')
        }),
        ('Status', {
            'fields': ('is_active', 'is_verified')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(OwnerOTP)
class OwnerOTPAdmin(admin.ModelAdmin):

    list_display = ['user', 'otp_code', 'is_used', 'created_at', 'expires_at']
    list_filter = ['is_used']
    search_fields = ['user__email', 'otp_code']
    readonly_fields = ['created_at']

