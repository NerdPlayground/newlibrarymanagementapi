from django.db import models

class Notification(models.Model):
    created_on= models.DateTimeField(auto_now_add=True)
    student= models.ForeignKey('students.Student',related_name='notifications',on_delete=models.CASCADE)
    title= models.CharField(max_length=255)
    message= models.TextField()
    read= models.BooleanField(default=False)