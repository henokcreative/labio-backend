from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ContactMessage
from .serializers import ContactMessageSerializer
import resend
import os
import logging

logger = logging.getLogger(__name__)
resend.api_key = os.environ.get('RESEND_API_KEY')

@api_view(['GET'])
def get_messages(request):
    """Get all submitted contact messages (for development/admin only)"""
    messages = ContactMessage.objects.all().order_by('-submitted_at')
    serializer = ContactMessageSerializer(messages, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def submit_contact(request):
    serializer = ContactMessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        try:
            resend.Emails.send({
                "from": os.environ.get('EMAIL_FROM', 'noreply@yourdomain.com'),
                "to": os.environ.get('CONTACT_EMAIL', 'henok.karvonen@gmail.com'),
                "subject": f"New contact from {request.data.get('name')}",
                "text": f"Name: {request.data.get('name')}\nEmail: {request.data.get('email')}\nMessage: {request.data.get('message')}"
            })
        except Exception as e:
            logger.error(f"Email failed: {e}")
        return Response({'message': 'Message received!'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



