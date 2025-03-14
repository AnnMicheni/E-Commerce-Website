from django.db import models

# Create your models here.
class Product_Management (models.Model):
    id = models.CharField(max_length=10)
    description = models.CharField(max_length=255)
    price = models.CharField(max_length=10)
    stock = models.CharField(max_length=10)
    category = models.CharField(max_length=20)
    image = models.CharField(max_length=10)
    created_at = models.CharField(max_length=20)
    updated_at = models.CharField(max_length=20)

    