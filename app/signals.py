'''
Signal Receivers:
These are functions that get called when a certain event (signal) happens. In this case, the events are post_save signals for the User model. 
The create_user_profile function is called when a new user is created, and it creates a corresponding Profile for that user. The save_user_profile 
function is called every time a user's details are saved, and it ensures that the user's profile is also saved.
'''
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
