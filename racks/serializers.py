from racks.models import Rack
from book_items.models import BookItem
from rest_framework import serializers

class AddRackSerializer(serializers.ModelSerializer):
    class Meta:
        model= Rack
        fields= ["id","floor","segment","position","rack_number"]

class ViewRackSerializer(serializers.HyperlinkedModelSerializer):
    book_items= serializers.HyperlinkedRelatedField(many=True,view_name="view-book-item",read_only=True)
    class Meta:
        model= Rack
        fields= ["id","floor","segment","position","rack_number","book_items"]