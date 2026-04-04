from django.db import models

# Create your models here.
class Client(models.Model):
    first_name  = models.CharField(max_length=64)
    last_name   = models.CharField(max_length=64)
    register_at = models.DateTimeField()