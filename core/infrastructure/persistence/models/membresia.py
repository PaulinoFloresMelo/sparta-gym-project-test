# infrastructure/persistence/models/membresia.py
from django.db import models

class Membresia(models.Model):
    tipo = models.CharField(max_length=100)
    duracion_dias = models.IntegerField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    activa = models.BooleanField(default=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    promocion = models.BooleanField(default=False)
