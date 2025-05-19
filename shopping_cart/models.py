from django.db import models
from django.contrib.auth import get_user_model
from product_management.models import Product
from Utils.models import BaseModel

User = get_user_model()

class CartItem(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,to_field='id')
    quantity = models.PositiveIntegerField(default=1)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
