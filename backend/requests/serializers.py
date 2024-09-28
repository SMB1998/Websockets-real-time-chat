from rest_framework import serializers
from .models import Requests
from users.models import Users
from components.models import Components

# Serializador para el modelo Users
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        exclude = ['password']  # Excluir el campo de contraseña


# Serializador para el modelo Components
class ComponentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Components
        fields = '__all__'

# Serializador para el modelo Requests
class RequestsSerializer(serializers.ModelSerializer):
    # admin = UsersSerializer(many=True)  # Incluir el serializador de Users para el campo admin
    # users = UsersSerializer(many=True)  # Incluir el serializador de Users para el campo users
    # components = ComponentsSerializer(many=True)  # Incluir el serializador de Components para el campo components

    class Meta:
        model = Requests
        fields = '__all__'