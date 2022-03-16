from authors.models import Author
from rest_framework import serializers

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model= Author
        fields= ["id","name","description"]

class ViewAuthorSerializer(serializers.HyperlinkedModelSerializer):
    books= serializers.HyperlinkedRelatedField(many=True,view_name="view-book",read_only=True)
    class Meta:
        model= Author
        fields= ["id","name","description","books"]