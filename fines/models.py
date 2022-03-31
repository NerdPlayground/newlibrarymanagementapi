import uuid
from django.db import models

class Fine(models.Model):
    id= models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    created_at= models.DateField(auto_now_add=True)
    transaction= models.OneToOneField(
        'transactions.Transaction',
        related_name='transaction',
        on_delete=models.DO_NOTHING
    )
    amount= models.IntegerField()
    last_updated= models.DateField(null=True,blank=True)
    paid= models.BooleanField(default=False)
    paid_on= models.DateField(null=True,blank=True)

    def __str__(self):
        return str(self.transaction)