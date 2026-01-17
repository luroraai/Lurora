#  Author : Wosvo Interactive
#  Developer : Fürkan Göktaş
#  Email : furkan@wosvo.com
#  Date : 24.03.2025 12:51
#  Filename : signals.py
#  Last Modified : 24.03.2025 12:51
#  Project : backend
#  Module : backend
# 
#  Copyright (c) 2025

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create or update user profile when a user is created or updated.
    """
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()

# Ensure the signal is connected
post_save.connect(create_or_update_user_profile, sender=User)