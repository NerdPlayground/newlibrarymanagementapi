from rest_framework import serializers
from transactions.models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model= Transaction
        fields= ["id","student","book_item","issued_at","due_date","returned_at"]