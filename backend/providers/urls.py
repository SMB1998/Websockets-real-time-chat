from django.urls import path
from .views import ProvidersListCreateView, ProvidersRetrieveUpdateDestroyView

urlpatterns = [
    path('providers/', ProvidersListCreateView.as_view(), name='providers-list-create'),
    path('providers/<str:pk>/', ProvidersRetrieveUpdateDestroyView.as_view(), name='provider-detail'),
]
