from racks.models import Rack
from book_items.models import BookItem
from rest_framework import serializers

class AddRackSerializer(serializers.ModelSerializer):
    class Meta:
        model= Rack
        fields= ["id","floor","segment","position","rack_number"]

class ViewRackSerializer(serializers.ModelSerializer):
    book_items= serializers.PrimaryKeyRelatedField(many=True,queryset=BookItem.objects.all())
    class Meta:
        model= Rack
        fields= ["id","floor","segment","position","rack_number","book_items"]