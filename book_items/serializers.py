from book_items.models import BookItem
from rest_framework import serializers

class BookItemSerializer(serializers.ModelSerializer):
    class Meta:
        model= BookItem
        fields= ['id','book','reference','status','purchased_on','published_on']