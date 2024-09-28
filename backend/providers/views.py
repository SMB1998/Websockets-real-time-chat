from rest_framework import generics
from .models import Providers
from .serializers import ProvidersSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

@permission_classes([IsAuthenticated])
class ProvidersListCreateView(generics.ListCreateAPIView):
    queryset = Providers.objects.all()
    serializer_class = ProvidersSerializer

@permission_classes([IsAuthenticated])
class ProvidersRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Providers.objects.all()
    serializer_class = ProvidersSerializer