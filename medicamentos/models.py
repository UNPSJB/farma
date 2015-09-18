from django.db import models
from django.utils import timezone

# Create your models here.

class Monodroga(models.Model):
    FILTROS = ["nombre__icontains"]
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Dosis(models.Model):
    monodroga = models.ForeignKey('Monodroga')
    unidadMedida = models.CharField(max_length=100)
    cantidad = models.IntegerField()

    def __str__(self):
        return self.unidadMedida



