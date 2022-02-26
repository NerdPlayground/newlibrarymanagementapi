from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator

class RegisterSerializer(serializers.Serializer):
    first_name= serializers.CharField(max_length=150)
    last_name= serializers.CharField(max_length=150)
    username= serializers.CharField(max_length=150)
    email= serializers.EmailField(max_length=150)
    password= serializers.CharField(min_length=8,max_length=20,write_only=True)

class LoginSerializer(serializers.Serializer):
    id= serializers.IntegerField(read_only=True)
    username= serializers.CharField(max_length=150)
    password= serializers.CharField(min_length=8,max_length=20,write_only=True)

class UserSerializer(serializers.Serializer):
    id= serializers.IntegerField(read_only=True)
    first_name= serializers.CharField(max_length=150)
    last_name= serializers.CharField(max_length=150)
    username= serializers.CharField(max_length=150)
    email= serializers.EmailField(max_length=150)