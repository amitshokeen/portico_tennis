from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Add custom fields if needed, e.g., phone_number = models.CharField(max_length=15)
    phone_number = models.CharField(max_length=12, blank=True, null=True)

    def __str__(self):
        return self.username

# Create your models here.
