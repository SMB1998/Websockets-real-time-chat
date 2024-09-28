from django.urls import path
from .views import QueuesListCreateView, QueuesRetrieveUpdateDestroyView

urlpatterns = [
    path('queue_request/', QueuesListCreateView.as_view(), name='queues-list-create'),
    path('queue_request/<str:pk>/', QueuesRetrieveUpdateDestroyView.as_view(), name='queues-detail'),
]
