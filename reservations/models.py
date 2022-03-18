from django.db import models

class Reservation(models.Model):
    reserved_on= models.DateField(auto_now_add=True)
    student= models.ForeignKey('students.Student',related_name='reservations',on_delete=models.CASCADE)
    book_item= models.ForeignKey('book_items.BookItem',related_name='reservations',on_delete=models.DO_NOTHING)
    status= models.CharField(default='Pending',max_length=255)