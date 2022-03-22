from dataclasses import fields
from rest_framework import serializers
from notifications.models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model= Notification
        fields= ["created_on","student","title","message","read"]