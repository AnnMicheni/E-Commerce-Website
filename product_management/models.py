from django.db import models, migrations
from Utils.models import BaseModel

class Product(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def custom_migration(product_management, schema_editor):
        pass

    def __str__(self):
        return self.name
