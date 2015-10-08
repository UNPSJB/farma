from django.db import models

class Farmacia(models.Model):
    FILTROS = ["razonSocial__icontains"]
    razonSocial = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    mail = models.CharField(max_length=50, blank=True)
    localidad= models.CharField(max_length=50)
    nombreEncargado = models.CharField(max_length=80, blank=True)
    telefono = models.CharField(max_length=80, blank=True)
    cuit = models.CharField(max_length=80)

    def __str__(self):
        return self.razonSocial

class Clinica(models.Model):
    FILTROS = ["razonSocial__icontains"]
    razonSocial = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    mail = models.CharField(max_length=50)
    localidad= models.CharField(max_length=50)
    obraSocial = models.CharField(max_length=80)
    telefono = models.CharField(max_length=80)
    cuit = models.CharField(max_length=80)

    def __str__(self):
        return self.razonSocial

class Laboratorio(models.Model):

    FILTROS = ["razonSocial__icontains"]
    razonSocial = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    mail = models.CharField(max_length=50)
    localidad= models.CharField(max_length=50)
    telefono = models.CharField(max_length=80)
    cuit = models.CharField(max_length=80)

    def __str__(self):
        return self.razonSocial