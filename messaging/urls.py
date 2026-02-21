from django.urls import path
from . import views

urlpatterns = [
    path('conversations/', views.get_conversations, name='get_conversations'),
    path('conversations/<int:conversation_id>/send/', views.send_message, name='send_message'),
]