from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_conversations(request):
    if request.user.is_staff:
        conversations = Conversation.objects.all().order_by('-updated_at')
    else:
        conversations = Conversation.objects.filter(client=request.user).order_by('-updated_at')
    serializer = ConversationSerializer(conversations, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request, conversation_id):
    try:
        if request.user.is_staff:
            conversation = Conversation.objects.get(id=conversation_id)
        else:
            conversation = Conversation.objects.get(id=conversation_id, client=request.user)
    except Conversation.DoesNotExist:
        return Response({'error': 'Conversation not found'}, status=status.HTTP_404_NOT_FOUND)

    message = Message.objects.create(
        conversation=conversation,
        sender=request.user,
        body=request.data.get('body')
    )
    # Mark all messages as read when staff replies
    if request.user.is_staff:
        conversation.messages.filter(is_read=False).update(is_read=True)

    serializer = MessageSerializer(message)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_read(request, conversation_id):
    if not request.user.is_staff:
        return Response({'error': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
    Conversation.objects.get(id=conversation_id).messages.filter(is_read=False).update(is_read=True)
    return Response({'status': 'marked read'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assign_staff(request, conversation_id):
    if not request.user.is_staff:
        return Response({'error': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
    try:
        conversation = Conversation.objects.get(id=conversation_id)
        conversation.assigned_staff = request.user
        conversation.save()
        return Response({'status': 'assigned', 'staff': request.user.username})
    except Conversation.DoesNotExist:
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_conversation(request):
    if not request.user.is_staff:
        return Response({'error': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
    client_id = request.data.get('client_id')
    subject = request.data.get('subject')
    try:
        client = User.objects.get(id=client_id, is_staff=False)
    except User.DoesNotExist:
        return Response({'error': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)
    conversation = Conversation.objects.create(
        client=client,
        subject=subject,
        assigned_staff=request.user
    )
    serializer = ConversationSerializer(conversation)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def unread_count(request):
    count = Message.objects.filter(
        conversation__client=request.user,
        is_read=False
    ).exclude(sender=request.user).count()
    return Response({'unread': count})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_clients(request):
    if not request.user.is_staff:
        return Response({'error': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
    clients = User.objects.filter(is_staff=False, is_active=True).values('id', 'username', 'first_name', 'last_name')
    return Response(list(clients))