from book_items.models import BookItem
from rest_framework import serializers

class BookItemSerializer(serializers.ModelSerializer):
    class Meta:
        model= BookItem
        fields= [
            "id","book","reference","loaned_to","reserved_by",
            "status","purchased_on","published_on","rack"
        ]
        read_only_fields = ["purchased_on"]