import uuid
from django.db import models

class Notification(models.Model):
    id= models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    created_on= models.DateTimeField(auto_now_add=True)
    student= models.ForeignKey(
        'students.Student',
        related_name='notifications',
        on_delete=models.CASCADE
    )
    title= models.CharField(max_length=255)
    message= models.TextField()
    read= models.BooleanField(default=False)

    def __str__(self):
        return self.title