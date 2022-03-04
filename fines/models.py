from django.db import models
from django.utils import timezone

class Fine(models.Model):
    created_at= models.DateTimeField(auto_now_add=True)
    student= models.ForeignKey('students.Student',related_name='fines',on_delete=models.DO_NOTHING)
    transaction= models.OneToOneField('transactions.Transaction',related_name='transaction',on_delete=models.DO_NOTHING)
    amount= models.IntegerField()
    paid= models.BooleanField(default=False,null=True,blank=True)
    paid_on= models.DateTimeField(null=True,blank=True)