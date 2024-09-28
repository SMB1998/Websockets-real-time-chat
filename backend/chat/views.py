# chat/views.py
# chat/views.py

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Message, Room
from .serializers import MessageSerializer

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer

    def get_queryset(self):
        room_id = self.request.query_params.get('room', None)
        if room_id is not None:
            return Message.objects.filter(room_id=room_id)
        return Message.objects.all()

    def perform_create(self, serializer):
        serializer.save()

