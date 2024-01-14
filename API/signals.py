from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import EmailConfirmationToken, CustomUser
from django.apps import apps
from .functions import send_confirmation_email


@receiver(post_save, sender=CustomUser)
def create_email_confirmation_token(sender, instance, created, **kwargs):
    if created:
        token = EmailConfirmationToken.objects.create(user=instance)
        send_confirmation_email(instance, token)


def connect_signals(sender, **kwargs):
    if apps.ready:
        post_save.connect(create_email_confirmation_token, sender=CustomUser)

