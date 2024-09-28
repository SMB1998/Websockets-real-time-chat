from rest_framework import serializers
from .models import QueueReuqest
from users.models import Users
from components.models import Components

# Serializador para el modelo Users
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        exclude = ['password']  # Excluir el campo de contraseña


# Serializador para el modelo Queues
class QueueReuqestSerializer(serializers.ModelSerializer):
    users = UsersSerializer(many=True)  # Incluir el serializador de Users para el campo users
    class Meta:
        model = QueueReuqest
        fields = '__all__'