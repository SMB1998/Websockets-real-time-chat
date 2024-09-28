from django.db import models
import uuid 
from users.models import Users
from components.models import Components

class Queues(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    users = models.ManyToManyField(Users, related_name='queues_users', blank=True)     
    components = models.ManyToManyField(Components, related_name='queues_components', blank=True)     
    referencia = models.CharField(max_length=100, blank=True)
    nombre = models.CharField(max_length=100)
    admin = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='admin_queues', blank=True) 
    autoacept = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre