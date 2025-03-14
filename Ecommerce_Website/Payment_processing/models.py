from django.db import models

# Create your models here.
class Payment_processing(models.Model):
    id = models.CharField(max_length=10)
    userkey = models.CharField(max_length=20)
    orderkey = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=20)
    transactionid = models.CharField(max_length=20)
    amount = models.CharField(max_length=10)
    status = models.CharField(max_length= 20)
    paymentdate = models.CharField(max_length= 20)