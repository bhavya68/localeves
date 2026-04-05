from django.db import models

# Create your models here.
# File: events/models.py

from django.db import models
from django.conf import settings
from django.utils import timezone
from establishments.models import Establishment
from chat.models import ChatRoom


class Event(models.Model):
    establishment = models.ForeignKey(
        Establishment, on_delete=models.CASCADE, related_name='events'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, related_name='created_events'
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    chat_room = models.OneToOneField(
        ChatRoom, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='event'
    )
    razorpay_order_id = models.CharField(max_length=100, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True)
    amount_paid = models.PositiveIntegerField(default=0)
    is_payment_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_datetime']

    def __str__(self):
        return f'{self.name} @ {self.establishment.name}'

    def is_live(self):
        now = timezone.now()
        return (
            self.is_payment_verified and
            self.is_active and
            self.start_datetime <= now <= self.end_datetime
        )