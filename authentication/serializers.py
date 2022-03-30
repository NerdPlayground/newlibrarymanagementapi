from books.models import Book
from rest_framework import serializers
from transactions.models import Transaction
from django.contrib.auth.models import User

class RegisterPatronSerializer(serializers.Serializer):
    first_name= serializers.CharField(max_length=150)
    last_name= serializers.CharField(max_length=150)
    registration_number= serializers.CharField(max_length=150)
    email= serializers.EmailField(max_length=150)
    password= serializers.CharField(min_length=8,max_length=20,write_only=True)

class PatronSerializer(serializers.Serializer):
    id= serializers.IntegerField(read_only=True)
    first_name= serializers.CharField(max_length=150)
    last_name= serializers.CharField(max_length=150)
    username= serializers.CharField(max_length=150)
    email= serializers.EmailField(max_length=150)

class EditPatronSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields= ["first_name","last_name","email"]