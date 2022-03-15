from rest_framework import serializers
from library_cards.models import LibraryCard

class LibraryCardSerializer(serializers.ModelSerializer):
    class Meta:
        model= LibraryCard
        fields= ["student","issued_at","active"]

class LibraryCardStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model= LibraryCard
        fields= ["active"]