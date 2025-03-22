from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    #phone_number = models.CharField(max_length=15, blank=True, null=True)
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('staff', 'Staff'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='staff')