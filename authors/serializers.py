from authors.models import Author
from rest_framework import serializers

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model= Author
        fields= ["id","name","description"]

class ViewAuthorSerializer(serializers.ModelSerializer):
    books= serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    class Meta:
        model= Author
        fields= ["id","name","description","books"]