# En tu_app/models.py
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save


from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Users(AbstractUser):
    ADMIN = 'admin'
    CLIENTE = 'cliente'
    SELLER = 'seller'
    ROLE_CHOICES = [
        (ADMIN, 'Administrador'),
        (CLIENTE, 'Cliente'),
        (SELLER, 'seller'),
    ]
    displayName = models.CharField(max_length=100, blank=True, null=True, default=None)
    photo = models.CharField(max_length=100, blank=True, null=True, default=None)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=CLIENTE)
    


    def __str__(self):
        return self.username
    

    
#quitar este reciver para hacer el createsuperuser    , sirve para hashear la pasword
# @receiver(pre_save, sender=Users)
# def hash_user_password(sender, instance, **kwargs):
#         if instance._state.adding:  # Verifica si se está creando un nuevo objeto
#             instance.password = make_password(instance.password)
        