from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Add custom fields if needed, e.g., phone_number = models.CharField(max_length=15)
    phone_number = models.CharField(max_length=12)

# Create your models here.
