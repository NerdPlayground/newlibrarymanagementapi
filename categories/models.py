import uuid
from django.db import models

class Category(models.Model):
    id= models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name= models.CharField(max_length=255)
    description= models.TextField()

    def __str__(self):
        return self.name