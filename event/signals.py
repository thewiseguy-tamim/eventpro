from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Event

@receiver(m2m_changed, sender=Event.participants.through)
def send_rsvp_notification(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        user = instance.participants.get(id__in=pk_set)
        send_mail(
            'RSVP Confirmation',
            f'You have successfully RSVPed to {instance.event_name}.',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )