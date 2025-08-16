from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.CharField(max_length=280, blank=True)
    avatar_url = models.URLField(blank=True)

    def __str__(self):
        return f"Profile({self.user.username})"

# Create your models here.
