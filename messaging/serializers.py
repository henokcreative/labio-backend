from rest_framework import serializers
from .models import Conversation, Message

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'body', 'sender_username', 'is_read', 'created_at']

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    client_username = serializers.CharField(source='client.username', read_only=True)
    
    class Meta:
        model = Conversation
        fields = ['id', 'subject', 'client_username', 'created_at', 'updated_at', 'messages']