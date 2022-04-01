from pyexpat import model
from students.models import Student
from rest_framework import serializers
from transactions.models import Transaction

class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model= Student
        fields= ["registration_number","campus","faculty","course","mode_of_study"]

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model= Student
        fields= ["id","first_name","last_name","registration_number","campus","faculty","course","mode_of_study"]

class PatronActivitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model= Transaction
        fields= ["student","book_item","issued_at","due_date","returned_at"]
        read_only_fields= ["student","due_date"]