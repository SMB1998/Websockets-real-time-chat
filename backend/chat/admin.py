from django.contrib import admin
from .models import Room
# Register your models here.
from .models import Message
admin.site.register(Room)
admin.site.register(Message)