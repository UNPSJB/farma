# - encode: utf-8 -
from django.db import models
from organizaciones.models import Laboratorio
from django.core.validators import MaxValueValidator, MinValueValidator
from pedidos import config
import datetime


class Medicamento(models.Model):
    FILTROS = ["nombreFantasia__nombreF__icontains", 'laboratorio__razonSocial__icontains']
    formulas = models.ManyToManyField('Monodroga',  through='Dosis')
    nombreFantasia = models.ForeignKey('NombreFantasia')
    presentacion = models.ForeignKey('Presentacion')
    codigoBarras = models.CharField("Codigo de barras", max_length=15, unique=True, error_messages={'unique': "Este codigo de barras ya esta cargado"})
    laboratorio = models.ForeignKey(Laboratorio, related_name="medicamentos")
    stockMinimo = models.PositiveIntegerField("Stock minimo de reposicion")
    precioDeVenta = models.FloatField("Precio de venta", validators=[MinValueValidator(0.0), MaxValueValidator(9999)])

    def __str__(self):
        return "%s %s" % (self.nombreFantasia, self.presentacion)

    def get_stock(self):
        if self.id:
            stockTotal = 0
            lotes = self.get_lotes_activos()
            for lote in lotes:
                stockTotal += lote.stock
            return stockTotal

    def get_lotes_activos(self):
        if self.id:
            lim = datetime.date.today() + datetime.timedelta(weeks=config.SEMANAS_LIMITE_VENCIDOS)
            return Lote.objects.filter(medicamento=self, stock__gt=0, fechaVencimiento__gte=lim)
        return None



class Presentacion(models.Model):
    FILTROS = ["descripcion__icontains"]
    descripcion = models.TextField(max_length=95)
    cantidad = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1),MaxValueValidator(9999)])
    unidadMedida = models.CharField("Unidad de medida", max_length=45)

    def __str__(self):
        return "%s - %s %s" % (self.descripcion, self.cantidad, self.unidadMedida)


class Formula(models.Model):
    monodroga = models.ForeignKey('Monodroga')
    dosis = models.ForeignKey('Dosis')


class Monodroga(models.Model):
    FILTROS = ["nombre__icontains"]
    nombre = models.CharField(max_length=75, unique=True, error_messages={'unique': "Esta monodroga ya esta cargada"})

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
    nombreF = models.CharField(max_length=75,unique=True,error_messages={'unique': "Este nombre de fantasia ya esta cargado!"})

    def __str__(self):
        return "%s" % self.nombreF


class Lote(models.Model):
    FILTROS = ["numero__icontains"]
    numero = models.PositiveIntegerField(unique=True, error_messages={'unique': "Este numero de lote ya esta cargado!"})
    fechaVencimiento= models.DateField()
    stock = models.PositiveIntegerField()
    precio = models.FloatField()
    medicamento = models.ForeignKey('Medicamento', on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.numero

    def to_json(self):
        if self.numero:
            return {
                'nroLote': self.numero,
                'fechaVencimiento': self.fechaVencimiento.strftime("%d/%m/%y"),
                'stock': self.stock
            }









