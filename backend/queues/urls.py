from django.urls import path
from .views import QueuesListCreateView, QueuesRetrieveUpdateDestroyView, UserQueuesView

urlpatterns = [
    path('queues/', QueuesListCreateView.as_view(), name='queues-list-create'),
    path('queues/<str:pk>/', QueuesRetrieveUpdateDestroyView.as_view(), name='queues-detail'),
    path('my-queues/', UserQueuesView.as_view(), name='user-queues'),
]
