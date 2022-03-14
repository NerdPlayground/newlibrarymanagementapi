from django.db import models

class BookItem(models.Model):
    book= models.ForeignKey('books.Book',related_name='book_items',on_delete=models.CASCADE)
    reference= models.BooleanField(default=False)
    status= models.CharField(max_length=255)
    purchased_on= models.DateField()
    published_on= models.DateField()
    rack= models.ForeignKey('racks.Rack',related_name='book_items',on_delete=models.DO_NOTHING)