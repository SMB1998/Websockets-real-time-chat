from django.db import models
import uuid 
from users.models import Users
from components.models import Components

class Status(models.TextChoices):
    """
    Defines the possible status options for a request.
    """
    RECIBIDO = 'RECIBIDO', 'Recibido'  # Received
    ALISTANDO = 'ALISTANDO', 'Alistando'  # Preparing
    ENVIADO = 'ENVIADO', 'Enviado'  # Sent
    ENTREGADO = 'ENTREGADO', 'Entregado'

class Requests(models.Model):
    id = models.AutoField(primary_key=True, unique=True, editable=False)
    # users = models.ManyToManyField(Users, related_name='requests_users', blank=True)     
    # components = models.ManyToManyField(Components, related_name='requests_components', blank=True)     
    referencia = models.CharField(max_length=100, blank=True)
    nombre = models.CharField(max_length=100)
    # admin = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='admin_requests', blank=True) 
    status = models.CharField(
            max_length=20,
            choices=Status.choices,
            default=Status.RECIBIDO,  # Set default status to "recibido"
        )

    def __str__(self):
        return self.nombre

    def get_custom_id(self):
        return f'KNOT{self.id}'