from books.models import Book
from categories.models import Category
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    books= serializers.PrimaryKeyRelatedField(many=True,queryset=Book.objects.all())
    class Meta:
        model= Category
        fields= ["category_name","books"]