from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    google_id = models.CharField(max_length=255, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return '/static/frontend/images/user/user1.png'

    def get_story_count(self):
        return self.stories.count()

    def get_shared_story_count(self):
        return self.stories.filter(status='published').count()


class Profile(models.Model):
    STATUS_CHOICES = (('active', 'Active'), ('inactive', 'Inactive'),)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    followers = models.ManyToManyField(User, related_name='following')
    following = models.ManyToManyField(User, related_name='followed_by')
    story_limit = models.PositiveIntegerField(default=10, blank=True, null=True)
    story_count = models.PositiveIntegerField(default=0, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f'Profile for {self.user.email}'
