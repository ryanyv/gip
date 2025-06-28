
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.templatetags.static import static

USER_ROLES = [
    ('superadmin', 'Super Admin'),
    ('admin', 'Admin'),
    ('user', 'User'),
]

def user_avatar_path(instance, filename):
    # Files uploaded to MEDIA_ROOT/avatars/user_<id>/<filename>
    return f"avatars/user_{instance.id}/{filename}"

class User(AbstractUser):
    # Add extra fields for your custom user
    profile_photo = models.ImageField(upload_to=user_avatar_path, blank=True, null=True)
    role = models.CharField(max_length=20, choices=USER_ROLES, default='user')
    position = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, blank=True, null=True)
    no_commercial_emails = models.BooleanField(default=False)
    agreed_tos = models.BooleanField(default=False)
    is_team_member = models.BooleanField(default=False)
    bio = models.TextField(blank=True, null=True)

    @property
    def profile_photo_url(self):
        """Return the URL for the user's profile photo or the default image."""
        if self.profile_photo:
            return self.profile_photo.url
        return static('photos/default_profile_image.png')

    def __str__(self):
        return self.get_full_name() or self.username

    @property
    def is_superadmin(self):
        return self.role == 'superadmin'

    @property
    def is_admin(self):
        return self.role == 'admin' or self.role == 'superadmin'
