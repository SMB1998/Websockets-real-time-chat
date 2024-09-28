from django.db import models
from rest_framework import serializers
import uuid 
from providers.models import Providers



    
class Components(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    proveedor = models.ForeignKey(Providers, on_delete=models.CASCADE, related_name='providers') 
    url = models.URLField(max_length=200)
    referencia = models.CharField(max_length=100, blank=True)
    precio = models.CharField(max_length=100, blank=True)
    nombre = models.CharField(max_length=100)
    image_url = models.CharField(max_length=250, blank=True)
    datasheet_url = models.CharField(max_length=250, blank=True)
    search_index_provider = models.CharField(max_length=100, blank=True, null=True)  # Nuevo campo para el nombre del proveedor
    def __str__(self):
        return f"{self.id} - {self.nombre} - {self.referencia}"

    # def save(self, *args, **kwargs):
    #     if self.proveedor:
    #         self.search_index_provider = self.proveedor.nombre  # Actualiza el campo con el nombre del proveedor
    #     super().save(*args, **kwargs)