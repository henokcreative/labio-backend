from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ContactMessage
from .serializers import ContactMessageSerializer
import resend
import os

resend.api_key = os.environ.get('RESEND_API_KEY')

@api_view(['POST'])
def submit_contact(request):
    serializer = ContactMessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        try:
            resend.Emails.send({
                "from": "onboarding@resend.dev",
                "to": "henok.karvonen@gmail.com",
                "subject": f"New contact from {request.data.get('name')}",
                "text": f"Name: {request.data.get('name')}\nEmail: {request.data.get('email')}\nMessage: {request.data.get('message')}"
            })
        except Exception as e:
            print(f"Email failed: {e}")
        return Response({'message': 'Message received!'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



