from django.core.management.base import BaseCommand
from django.utils import timezone
from events.models import Event


class Command(BaseCommand):
    help = 'Close expired events and their chat rooms'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        expired = Event.objects.filter(
            is_active=True,
            is_payment_verified=True,
            end_datetime__lt=now,
        )
        count = 0
        for event in expired:
            event.is_active = False
            event.save(update_fields=['is_active'])
            if event.chat_room:
                event.chat_room.is_active = False
                event.chat_room.save(update_fields=['is_active'])
            count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Closed {count} expired events.')
        )