from django.urls import path
from .views import RequestsListCreateView, RequestsRetrieveUpdateDestroyView

urlpatterns = [
    path('requests/', RequestsListCreateView.as_view(), name='requests-list-create'),
    path('requests/<str:pk>/', RequestsRetrieveUpdateDestroyView.as_view(), name='requests-detail'),
]
