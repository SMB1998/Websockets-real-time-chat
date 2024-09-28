# chat/models.py

from django.db import models
from users.models import Users

class Room(models.Model):
    name = models.CharField(max_length=255)
    participants = models.ManyToManyField(Users, related_name='rooms')
    is_private = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.content[:50]}'
