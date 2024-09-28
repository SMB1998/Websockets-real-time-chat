from rest_framework import generics
from .models import QueueReuqest
from .serializers import QueueReuqestSerializer


from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from rest_framework.pagination import LimitOffsetPagination

class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 35
    max_limit = 35  # Establece el límite máximo si lo deseas

@permission_classes([IsAuthenticated])
class QueuesListCreateView(generics.ListCreateAPIView):
    queryset = QueueReuqest.objects.all()
    serializer_class = QueueReuqestSerializer
    pagination_class = CustomLimitOffsetPagination  # Agrega paginación

@permission_classes([IsAuthenticated])
class QueuesRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = QueueReuqest.objects.all()
    serializer_class = QueueReuqestSerializer