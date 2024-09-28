from rest_framework import serializers
from .models import Queues
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

# Serializador para el modelo Queues
class QueuesSerializer(serializers.ModelSerializer):
    admin = UsersSerializer()  # Incluir el serializador de Users para el campo admin
    users = UsersSerializer(many=True)  # Incluir el serializador de Users para el campo users
    components = ComponentsSerializer(many=True)  # Incluir el serializador de Components para el campo components
    is_admin = serializers.SerializerMethodField()  # Campo personalizado is_admin

    class Meta:
        model = Queues
        fields = '__all__'

    def get_is_admin(self, obj):
        # Obtener el usuario que realiza la solicitud
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            # Comprobar si el usuario autenticado es el administrador de la cola
            print(obj, flush=True)
            b=obj.admin.id
            a=request.user.id
            _request = request 
            return obj.admin.id == request.user.id
        return False