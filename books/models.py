from django.db import models

class Book(models.Model):
    isbn= models.CharField(max_length=13,unique=True)
    category= models.ForeignKey('categories.Category',related_name='books',on_delete=models.CASCADE)
    name= models.CharField(max_length=255)
    description= models.TextField()
    author= models.CharField(max_length=255)
    published_on= models.DateField()
    publisher= models.CharField(max_length=255)
    language= models.CharField(max_length=255)
    pages= models.IntegerField()