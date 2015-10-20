from django.db import models

# Create your models here.
class RemitoMedVencido(models.Model):
    FILTROS = ["numero__icontains"]
    numero = models.BigIntegerField()
    fecha = models.DateField()
    #estado
    def __str__(self):
        return self.numero


class DetalleRemitoVencido(models.Model):
    FILTROS = ["numero__icontains"]
    numeroRemito = models.ForeignKey('RemitoMedVencido',on_delete = models.CASCADE)
    cantidad = models.BigIntegerField()
    #estado
    def __str__(self):
        return self.numero
