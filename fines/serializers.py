from fines.models import Fine
from rest_framework import serializers

class FineSerializer(serializers.ModelSerializer):
    class Meta:
        model= Fine
        fields= ["id","created_at","student","transaction","amount","paid","paid_on"]