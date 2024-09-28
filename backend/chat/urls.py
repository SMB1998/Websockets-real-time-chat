# chat/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageViewSet

# Crear un enrutador y registrar el ViewSet
router = DefaultRouter()
router.register(r'messages', MessageViewSet, basename='message')

# Incluir las rutas del enrutador
urlpatterns = [
    path('', include(router.urls)),
]
