from django.urls import path
from . import views

urlpatterns = [
    path('conversations/', views.get_conversations, name='get_conversations'),
    path('conversations/<int:conversation_id>/send/', views.send_message, name='send_message'),
    path('conversations/<int:conversation_id>/mark-read/', views.mark_read, name='mark_read'),
    path('conversations/<int:conversation_id>/assign/', views.assign_staff, name='assign_staff'),
    path('conversations/start/', views.start_conversation, name='start_conversation'),
    path('unread/', views.unread_count, name='unread_count'),
    path('clients/', views.get_clients, name='get_clients'),
]