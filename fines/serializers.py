from fines.models import Fine
from rest_framework import serializers

class FineSerializer(serializers.ModelSerializer):
    class Meta:
        model= Fine
        fields= ["id","created_at","transaction","amount","paid_on"]

class PayFineSerializer(serializers.Serializer):
    amount= serializers.IntegerField()