from students.models import Student
from rest_framework import serializers

class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model= Student
        fields= ["registration_number","campus","faculty","course","mode_of_study"]

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model= Student
        fields= ["first_name","last_name","registration_number","campus","faculty","course","mode_of_study"]
