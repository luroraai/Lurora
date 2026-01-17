#  Author : Wosvo Interactive
#  Developer : Fürkan Göktaş
#  Email : furkan@wosvo.com
#  Date : 8.04.2025 22:45
#  Filename : create_profiles.py
#  Last Modified : 8.04.2025 22:45
#  Project : backend
#  Module : backend
#
#  Copyright (c) 2025

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import Profile

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates missing profiles for existing users'

    def handle(self, *args, **options):
        users_without_profile = User.objects.filter(profile__isnull=True)
        for user in users_without_profile:
            Profile.objects.create(user=user)
            self.stdout.write(self.style.SUCCESS(f'Created profile for user: {user.email}'))
