from django.contrib import admin

# Register your models here.
# File: events/admin.py

from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'establishment', 'start_datetime', 'end_datetime', 'is_payment_verified', 'is_active', 'is_live_now']
    list_filter = ['is_active', 'is_payment_verified']
    search_fields = ['name', 'establishment__name']
    readonly_fields = ['razorpay_order_id', 'razorpay_payment_id', 'amount_paid', 'is_payment_verified', 'created_at', 'chat_room']

    def is_live_now(self, obj):
        return obj.is_live()
    is_live_now.boolean = True
    is_live_now.short_description = 'Live'