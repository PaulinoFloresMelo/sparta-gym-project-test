# src/infrastructure/persistence/models/sala.py
from django.db import models

class Sala(models.Model):
    nombre = models.CharField(max_length=100)
    capacidad = models.IntegerField()
    disponible = models.BooleanField(default=True)
