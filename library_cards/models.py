import uuid
from django.db import models

class LibraryCard(models.Model):
    id= models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    student= models.ForeignKey(
        'students.Student',
        related_name='library_card',
        on_delete=models.CASCADE
    )
    issued_at= models.DateField(auto_now_add=True)
    active= models.BooleanField()

    def __str__(self):
        return self.student.user.username