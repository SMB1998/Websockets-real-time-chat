from rest_framework import serializers
from .models import Components
from providers.models import Providers
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Providers
        fields = '__all__'  

class ComponentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Components
        fields = '__all__'
    
from rest_framework import serializers
from .documents import ComponentDocument

class ComponentDocumentSerializer(serializers.Serializer):
    nombre = serializers.CharField()
    referencia = serializers.CharField()
    search_index_provider = serializers.CharField()
    url = serializers.CharField()
    referencia = serializers.CharField()
    precio = serializers.CharField()
    nombre = serializers.CharField()
    image_url = serializers.CharField()
    datasheet_url = serializers.CharField()
    search_index_provider = serializers.CharField()
    proveedor = serializers.CharField()
    

    class Meta:
        model = Components
        fields = '__all__'
   