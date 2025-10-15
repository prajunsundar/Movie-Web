from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Person

@receiver(post_save, sender=User)
def create_person_profile(sender, instance, created, **kwargs):
    if created:
        Person.objects.create(user=instance)

