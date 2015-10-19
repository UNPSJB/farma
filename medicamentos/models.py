# - encode: utf-8 -
from django.db import models

# Create your models here.

class Medicamento(models.Model):
    FILTROS = ["codigoBarras__icontains"]
    formulas = models.ManyToManyField('Monodroga', through='Dosis')
    nombreFantasia = models.ForeignKey('NombreFantasia')
    presentacion = models.ForeignKey('Presentacion')
    codigoBarras = models.CharField("Codigo de barras", max_length=15)
    stockMinimo = models.IntegerField("Stock minimo de reposicion",
                                      help_text="Este es el stock minimo en el cual el sistema alertara de que es necesario realizar un pedido")
    precio = models.FloatField()

    def __str__(self):
        return self.codigoBarras


class Presentacion(models.Model):
    FILTROS = ["descripcion__icontains"]
    descripcion = models.TextField()
    cantidad = models.IntegerField()
    unidadMedida = models.CharField(max_length=50)

    def __str__(self):
        return "%s - %s %s" % (self.descripcion, self.cantidad, self.unidadMedida)

class Formula(models.Model):
    monodroga = models.ForeignKey('Monodroga')
    dosis = models.ForeignKey('Dosis') #on_delete = modelds.CASCADE


class Monodroga(models.Model):
    FILTROS = ["nombre__icontains"]
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return "%s" % self.nombre


class Dosis(models.Model):
    UNIDADES = (
        (1, "ml"),
        (2, "mg")
    )
    medicamento = models.ForeignKey(Medicamento)
    monodroga = models.ForeignKey(Monodroga)
    unidad = models.PositiveIntegerField(choices=UNIDADES)
    cantidad = models.IntegerField()

    def __str__(self):
        return "%s - %s" % (self.cantidad, self.get_unidad_display())

class NombreFantasia(models.Model):
    FILTROS = ["nombreF__icontains"]
    nombreF = models.CharField(max_length=100)

    def __str__(self):
        return "%s" % self.nombreF











