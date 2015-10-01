from django.db import models

# Create your models here.

class Medicamento(models.Model):
	formulas = models.ManyToManyField('Formula')
	nombreFantasia = models.ForeignKey('NombreFantasia')
	presentacion = models.ManyToManyField('Presentacion')
	codigoBarras = models.CharField(max_length=15)
	stockMinimo = models.IntegerField()
	precio = models.FloatField()
	
	def __str__(self):
		return self.codigoBarras

class NombreFantasia(models.Model):
	nombreF = models.CharField(max_length=30)		
	
	def __str__(self):
		return self.nombreF
	
class Presentacion(models.Model):
	descripcion = models.TextField()
	cantidad = models.IntegerField()
	unidadMedida = models.CharField(max_length=50)
	
	def __str__(self):
		return self.descripcion
		
class Formula(models.Model):
	monodroga = models.ForeignKey('Monodroga',on_delete = models.CASCADE)		
	dosis = models.ForeignKey('Dosis',on_delete = models.CASCADE)

	
class Monodroga(models.Model):
    #FILTROS = ["nombre__icontains"]
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Dosis(models.Model):
    unidadMedida = models.CharField(max_length=4)
    cantidad = models.IntegerField()




