from pyexpat import model
from django.db import models

class Category(models.Model):
    category_name= models.CharField(max_length=255)