from django.db import models

class Book(models.Model):
    book_name= models.CharField(max_length=255)
    book_author= models.CharField(max_length=255)
    book_category= models.ForeignKey('categories.Category',related_name='books',on_delete=models.CASCADE)