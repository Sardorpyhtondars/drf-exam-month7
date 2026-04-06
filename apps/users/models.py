from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Extended user model for the blog platform.

    Extra Fields:
    - bio: TextField, blank=True, null=True (short author biography)
    - avatar: ImageField, upload_to='avatars/', blank=True, null=True
    - website: URLField, blank=True, null=True (personal website link)

    __str__ returns: self.username
    """
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.username

