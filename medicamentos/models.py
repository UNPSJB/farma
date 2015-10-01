from django.db import models

# Create your models here.

class Monodroga(models.Model):
    FILTROS = ["nombre__icontains"]
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Dosis(models.Model):

    unidadMedida = models.CharField(max_length=100)
    cantidad = models.IntegerField()

    def __str__(self):
        return self.unidadMedida



class NombreFantasia(models.Model):
    FILTROS = ["nombre__icontains"]
    nombreF = models.CharField(max_length=100)


    def __str__(self):
        return self.nombre


class Presentacion(models.Model):
    FILTROS = ["descripcion__icontains"]
    descripcion = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    unidadMedida = models.CharField(max_length=100)


    def __str__(self):
        return self.descripcion







