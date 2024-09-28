from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Message, Room
from users.models import Users
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Unirse al grupo
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Aceptar la conexión WebSocket
        await self.accept()
        
         # Verificar si la sala existe
        room_exists = await self.room_exists(self.room_name)
        if not room_exists:
            # Si la sala no existe, cerrar la conexión y enviar un mensaje de error
            await self.send(text_data=json.dumps({
                'type': 'bad_room',
            })) 
            return

        # Recuperar mensajes históricos
        messages = await self.get_messages(self.room_name)

        # Enviar mensajes históricos al WebSocket
        await self.send(text_data=json.dumps({
            'type': 'initial_messages',
            'messages': messages
        }))

    async def disconnect(self, close_code):
        # Dejar el grupo
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_content = text_data_json.get('content', '')
        user_id = text_data_json.get('user', None)

        if not user_id:
            return  # Si no hay usuario, no procesar el mensaje

        user = await self.get_user(user_id)
        if not user:
            return  # Si el usuario no existe, no procesar el mensaje

        # Guardar el mensaje en la base de datos
        await self.save_message(message_content, user, self.room_name)

        # Recuperar todos los mensajes después de guardar el nuevo
        messages = await self.get_messages(self.room_name)

        # Enviar todos los mensajes al grupo
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'messages': messages  # Enviar todos los mensajes
            }
        )

    async def chat_message(self, event):
        messages = event['messages']

        # Enviar todos los mensajes al WebSocket
        await self.send(text_data=json.dumps({
            'type': 'all_messages',
            'messages': messages
        }))

    # Función para recuperar mensajes históricos
    @database_sync_to_async
    def get_messages(self, room_name):
        messages = Message.objects.filter(room__name=room_name)
        return [{'content': message.content, 'user': message.user.username} for message in messages]

    # Función para guardar un nuevo mensaje
    @database_sync_to_async
    def save_message(self, content, user, room_name):
        room = Room.objects.get(name=room_name)
        Message.objects.create(content=content, user=user, room=room)

    # Función para obtener un usuario por ID
    @database_sync_to_async
    def get_user(self, user_id):
        try:
            return Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            return None
    
       # Función para verificar si la sala existe
    @database_sync_to_async
    def room_exists(self, room_name):
        return Room.objects.filter(name=room_name).exists()
