from django.urls import path
from .views import ComponentsListCreateView, ComponentsRetrieveUpdateDestroyView
from . import views

urlpatterns = [
    path('components/', ComponentsListCreateView.as_view(), name='inventario-list-create'),
    path('components/<str:pk>/', ComponentsRetrieveUpdateDestroyView.as_view(), name='inventario-detail'),
    path('comp/search/', views.ComponentSearchView.as_view(), name='component-search'),
]
