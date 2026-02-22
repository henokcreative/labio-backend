from rest_framework import serializers
from .models import Conversation, Message
from django.contrib.auth.models import User

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'body', 'sender_username', 'is_read', 'created_at']

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    client_username = serializers.CharField(source='client.username', read_only=True)
    assigned_staff_username = serializers.CharField(source='assigned_staff.username', read_only=True, allow_null=True)
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'subject', 'client_username', 'assigned_staff_username', 'unread_count', 'created_at', 'updated_at', 'messages']

    def get_unread_count(self, obj):
        return obj.messages.filter(is_read=False).count()