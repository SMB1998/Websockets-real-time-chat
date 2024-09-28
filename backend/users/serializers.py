from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Users

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        # Verificar si el usuario existe y las credenciales son válidas
        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError('Credenciales inválidas')

        if not user.is_active:
            raise serializers.ValidationError('La cuenta de usuario está desactivada')

        return data