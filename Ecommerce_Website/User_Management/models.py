from django.db import models

# Create your models here.
class User_Management (models.Model):
    id = models.CharField (max_length=10)
    username = models.CharField (max_length=50)
    email = models.CharField (max_length=50)
    password = models.CharField (max_length=20)
    first_name = models.CharField (max_length=20)
    last_name = models.CharField (max_length=20)
    phone_number = models.CharField (max_length=20)
    address = models.CharField (max_length=20)
    role = models.CharField (max_length=20)
    date_joined = models.CharField (max_length=20)
    
