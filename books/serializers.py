from books.models import Book
from rest_framework import serializers

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model= Book
        fields= ["book_category","id","book_name","book_author"]