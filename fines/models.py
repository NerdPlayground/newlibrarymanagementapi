from django.db import models
from django.utils import timezone

class Fine(models.Model):
    created_at= models.DateField(auto_now_add=True)
    transaction= models.OneToOneField('transactions.Transaction',related_name='transaction',on_delete=models.DO_NOTHING)
    amount= models.IntegerField()
    paid_on= models.DateField(null=True,blank=True)