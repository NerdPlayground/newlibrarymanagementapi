from rest_framework import serializers
from transactions.models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model= Transaction
        fields= ["id","student","book","issued","issued_at","issued_by","returned","returned_at"]