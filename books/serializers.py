from books.models import Book
from book_items.models import BookItem
from rest_framework import serializers

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model= Book
        fields= [
            "id","isbn","category",
            "name","description","author",
            "published_on","publisher",
            "language","pages"
        ]

class ViewBookSerializer(serializers.ModelSerializer):
    book_items= serializers.PrimaryKeyRelatedField(many=True,queryset=BookItem.objects.all())
    class Meta:
        model= Book
        fields= [
            "id","isbn","category",
            "name","description","author",
            "published_on","publisher",
            "language","pages","book_items"
        ]