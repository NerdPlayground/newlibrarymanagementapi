from django.db import models

class Transaction(models.Model):
    student= models.ForeignKey('students.Student',related_name='transactions',on_delete=models.DO_NOTHING)
    book= models.OneToOneField('books.Book',related_name='transaction',on_delete=models.DO_NOTHING)
    issued= models.BooleanField(default=False)
    issued_at= models.DateTimeField()
    issued_by= models.ForeignKey('auth.User',related_name='transactions',on_delete=models.DO_NOTHING)
    returned= models.BooleanField(default=False)
    returned_at= models.DateTimeField()