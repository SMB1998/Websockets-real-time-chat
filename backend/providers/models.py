from django.db import models
from rest_framework import serializers
import uuid 


    
class Providers(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    nombre = models.CharField(max_length=100)
    # precio = models.CharField(max_length=100)  # Nuevo campo para el precio
    url = models.URLField(max_length=200)
    direccion = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    