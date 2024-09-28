from rest_framework import generics
from .models import Components
from .serializers import ComponentsSerializer, ComponentDocumentSerializer
from elasticsearch_dsl.query import MultiMatch, Bool , Term

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from rest_framework.pagination import LimitOffsetPagination

class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 35
    max_limit = 35  # Establece el límite máximo si lo deseas


class ComponentsListCreateView(generics.ListCreateAPIView):
    queryset = Components.objects.all()
    serializer_class = ComponentsSerializer
    pagination_class = CustomLimitOffsetPagination  # Agrega paginación


class ComponentsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Components.objects.all()
    serializer_class = ComponentsSerializer
    


from .documents import ComponentDocument

from .models import Components

class ComponentSearchView(generics.ListAPIView):
    serializer_class = ComponentDocumentSerializer
    
    def get_queryset(self):
        bool_query = Bool()

        # Obtener el parámetro de búsqueda de la solicitud
        q = self.request.query_params.get('q', None)
        proveedor_id = self.request.query_params.get('provider_id', None)

        # Si se proporciona un término de búsqueda, añadirlo a la consulta
        if q:
            query = MultiMatch(query=q, fields=["*"], fuzziness="AUTO")
            bool_query.must.append(query)

        # Si se proporciona un ID de proveedor, filtrar por el proveedor usando Term
        if proveedor_id:
            proveedor_query = Term(proveedor=proveedor_id)
            bool_query.filter.append(proveedor_query)

        # Construir la consulta final
        if bool_query.must or bool_query.filter:
            queryset = ComponentDocument.search().query(bool_query)[0:1000]
        else:
            queryset = ComponentDocument.search().query('match_all')[0:1000]

        return queryset