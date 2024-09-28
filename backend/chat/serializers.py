# chat/serializers.py

from rest_framework import serializers
from .models import Message, Room
from users.models import Users

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username']

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'is_private']

class MessageSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all(), required=True)  # Asegúrate de que este campo esté aquí
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), required=True)

    class Meta:
        model = Message
        fields = ['id', 'room', 'user', 'content', 'timestamp']
