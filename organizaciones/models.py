from django.db import models

class Organizacion(models.Model):
    FILTROS = ["razonSocial__icontains"]
    razonSocial = models.CharField(max_length=50)
    cuit = models.CharField(max_length=80)
    localidad= models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    email = models.EmailField(max_length=50, blank=True)
    telefono = models.CharField(max_length=80, blank=True) 

    class Meta:
        abstract = True   

class Farmacia(Organizacion):
    nombreEncargado = models.CharField(max_length=80, blank=True)

    def __str__(self):
        return self.razonSocial

class Clinica(Organizacion):
    obraSocial = models.CharField(max_length=80)

    def __str__(self):
        return self.razonSocial

class Laboratorio(Organizacion):
    def __str__(self):
        return self.razonSocial