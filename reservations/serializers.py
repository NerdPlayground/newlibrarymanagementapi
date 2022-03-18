from rest_framework import serializers
from reservations.models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    student= serializers.ReadOnlyField(source='student.user.username')
    class Meta:
        model= Reservation
        fields= ["id","reserved_on","student","book_item","status"]