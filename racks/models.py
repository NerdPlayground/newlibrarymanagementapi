import uuid
from django.db import models

class Rack(models.Model):
    id= models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    floor= models.IntegerField()
    segment= models.CharField(max_length=255)
    position= models.CharField(max_length=255)
    rack_number= models.IntegerField(unique=True)

    def __str__(self):
        floor,segment,position= str(self.floor),self.segment,self.position
        superscript= "st" if int(floor) == 1 else "nd" if int(floor) == 2 else "rd" if int(floor) == 3 else "th"
        rack_details= floor+superscript+" Floor, "+segment+" Segment, "+position+" Position"
        return rack_details