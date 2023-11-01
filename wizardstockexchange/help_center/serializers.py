from rest_framework import serializers
from .models import ContactMessage
from .models import LiveChatMessage

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'subject', 'message']


class LiveChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiveChatMessage
        fields = ['id', 'sender_name', 'message', 'timestamp']