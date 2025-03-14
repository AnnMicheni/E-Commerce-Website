from django.db import models

# Create your models here.
class Shopping_Cart(models.Model):
    id = models.CharField(max_length=10)
    userkey = models.CharField(max_length=20)
    order_date = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    totalprice = models.CharField(max_length=10)