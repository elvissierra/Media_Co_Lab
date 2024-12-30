from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Organization
from .services import create_demo_team

@receiver(post_save, sender=Organization)
def handle_demo_organization(sender, instance, created, **kwargs):
    if created:
        create_demo_team(instance)
