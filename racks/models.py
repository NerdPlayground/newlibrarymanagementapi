from django.db import models

class Rack(models.Model):
    floor= models.IntegerField()
    segment= models.CharField(max_length=255)
    position= models.CharField(max_length=255)
    rack_number= models.IntegerField()