from rest_framework import generics
from .models import Queues
from .serializers import QueuesSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.db.models import Q

from rest_framework.pagination import LimitOffsetPagination

class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 35
    max_limit = 35  # Establece el límite máximo si lo deseas

@permission_classes([IsAuthenticated])
class QueuesListCreateView(generics.ListCreateAPIView):
    queryset = Queues.objects.all()
    serializer_class = QueuesSerializer
    pagination_class = CustomLimitOffsetPagination  # Agrega paginación

@permission_classes([IsAuthenticated])
class QueuesRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Queues.objects.all()
    serializer_class = QueuesSerializer
    
@permission_classes([IsAuthenticated])   
class UserQueuesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        print(user, flush=True)
        
        # Obtener las colas asociadas al usuario autenticado
        queues = Queues.objects.filter(Q(users=user) | Q(admin=user)).distinct()
        serializer = QueuesSerializer(queues, many=True, context={'request': request})
        return Response(serializer.data)