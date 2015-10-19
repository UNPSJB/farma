# - encode: utf-8 -
from django.db import models

# Create your models here.

class Medicamento(models.Model):
    formulas = models.ManyToManyField('Monodroga', through='Dosis')
    nombreFantasia = models.ForeignKey('NombreFantasia', help_text="Este es el Nombre Comercial del medicamento")
    presentacion = models.ForeignKey('Presentacion', help_text="Esta es la forma en la que se encuentra comercialmente el Medicamento")
    codigoBarras = models.CharField("Codigo de barras", max_length=15, help_text="Este es un valor numerico, el cual deberia ser la clave")
    stockMinimo = models.PositiveIntegerField("Stock minimo de reposicion",
                                      help_text="Este es el stock minimo en el cual el sistema alertara de que es necesario realizar un pedido")
    precio = models.FloatField(help_text="Este es el precio de venta del medicamento")

    def __str__(self):
        return self.codigoBarras


class Presentacion(models.Model):
    FILTROS = ["descripcion__icontains"]
    descripcion = models.TextField()
    cantidad = models.PositiveIntegerField()
    unidadMedida = models.CharField(max_length=50)

    def __str__(self):
        return "%s - %s %s" % (self.descripcion, self.cantidad, self.unidadMedida)

class Formula(models.Model):
    monodroga = models.ForeignKey('Monodroga',on_delete = models.CASCADE)
    dosis = models.ForeignKey('Dosis',on_delete = models.CASCADE)


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
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return "%s - %s" % (self.cantidad, self.get_unidad_display())

class NombreFantasia(models.Model):
    FILTROS = ["nombreF__icontains"]
    nombreF = models.CharField(max_length=100)

    def __str__(self):
        return "%s" % self.nombreF


class Lote(models.Model):
    FILTROS = ["numero__icontains"]
    numero = models.PositiveIntegerField()
    fechaVencimiento= models.DateField()
    stock=models.PositiveIntegerField()
    precio=models.FloatField()
    medicamento=models.ForeignKey('Medicamento', on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.nombreF









