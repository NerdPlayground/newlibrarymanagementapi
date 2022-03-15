from django.db import models

class LibraryCard(models.Model):
    student= models.ForeignKey('students.Student',related_name='library_card',on_delete=models.CASCADE)
    issued_at= models.DateField(auto_now_add=True)
    active= models.BooleanField()