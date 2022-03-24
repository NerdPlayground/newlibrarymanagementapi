import uuid
from django.db import models

class BookItem(models.Model):
    id= models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    book= models.ForeignKey(
        'books.Book',
        related_name='book_items',
        on_delete=models.CASCADE
    )
    reference= models.BooleanField(default=False)
    loaned_to= models.ForeignKey(
        'students.Student',
        related_name='loaned_book_items',
        on_delete=models.DO_NOTHING,
        null=True,blank=True
    )
    reserved_by= models.ForeignKey(
        'students.Student',
        related_name='reserved_book_items',
        on_delete=models.DO_NOTHING,
        null=True,blank=True
    )
    status= models.CharField(max_length=255)
    purchased_on= models.DateField()
    published_on= models.DateField()
    rack= models.ForeignKey(
        'racks.Rack',
        related_name='book_items',
        on_delete=models.DO_NOTHING
    )