import uuid
from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    id= models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user= models.OneToOneField(
        'auth.User',
        related_name='student',
        on_delete=models.CASCADE
    )
    first_name = models.CharField(max_length=255,blank=False)
    last_name= models.CharField(max_length=255,blank=False)
    registration_number= models.CharField(
        max_length=8,
        unique=True,
        blank=True
    )
    campus= models.CharField(max_length=255,blank=True)
    faculty= models.CharField(max_length=255,blank=True)
    course= models.CharField(max_length=255,blank=True)
    mode_of_study= models.CharField(max_length=255,blank=True)