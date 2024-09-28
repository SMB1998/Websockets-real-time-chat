from rest_framework import generics
from .models import Requests
from .serializers import RequestsSerializer


from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from rest_framework.pagination import LimitOffsetPagination

class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 35
    max_limit = 35  # Establece el límite máximo si lo deseas


class RequestsListCreateView(generics.ListCreateAPIView):
    queryset = Requests.objects.all()
    serializer_class = RequestsSerializer
    pagination_class = CustomLimitOffsetPagination  # Agrega paginación


class RequestsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Requests.objects.all()
    serializer_class = RequestsSerializer