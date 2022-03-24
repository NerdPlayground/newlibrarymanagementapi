import uuid
from django.db import models

class Rack(models.Model):
    id= models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    floor= models.IntegerField()
    segment= models.CharField(max_length=255)
    position= models.CharField(max_length=255)
    rack_number= models.IntegerField()