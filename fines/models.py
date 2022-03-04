from django.db import models

class Fine(models.Model):
    student= models.ForeignKey('students.Student',related_name='fines',on_delete=models.DO_NOTHING)
    transaction= models.OneToOneField('transactions.Transaction',related_name='transaction',on_delete=models.DO_NOTHING)
    amount= models.IntegerField()
    paid= models.BooleanField(default=False,null=True,blank=True)
    paid_on= models.DateTimeField(null=True,blank=True)