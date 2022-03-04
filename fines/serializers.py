from fines.models import Fine
from rest_framework import serializers

class FineSerializer(serializers.ModelSerializer):
    class Meta:
        model= Fine
        fields= ["id","student","transaction","amount","paid","paid_on"]