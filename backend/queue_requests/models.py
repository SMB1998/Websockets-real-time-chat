from django.db import models
import uuid 
from users.models import Users
from queues.models import Queues

class QueueReuqest(models.Model): 
    description = models.CharField(max_length=100, blank=True)
    accepted = models.BooleanField(default=False)
    

    def __str__(self):
        return self.description