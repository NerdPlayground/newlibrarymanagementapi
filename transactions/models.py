from django.db import models
import datetime

class Transaction(models.Model):
    student= models.ForeignKey('students.Student',related_name='transactions',on_delete=models.DO_NOTHING)
    book_item= models.ForeignKey('book_items.BookItem',related_name='transactions',on_delete=models.DO_NOTHING)
    issued_at= models.DateField(auto_now_add=True)
    due_date= models.DateField()
    returned_at= models.DateField(null=True,blank=True)