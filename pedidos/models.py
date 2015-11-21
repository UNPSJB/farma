from django.db import models

# Create your models here.

class Remito(models.Model):
    pedidoFarmacia = models.ForeignKey('PedidoFarmacia', on_delete=models.CASCADE)
    fecha = models.DateField()

    def __str__(self):
        return str(self.id)

class DetalleRemito(models.Model):
    remito = models.ForeignKey(Remito, on_delete=models.CASCADE)
    cantidad = models.BigIntegerField()
    detallePedidoFarmacia = models.ForeignKey('DetallePedidoFarmacia')
    lote = models.ForeignKey('medicamentos.Lote')

    def __str__(self):
        return str(self.id)

class RemitoMedVencido(models.Model):
    numero = models.BigIntegerField()
    fecha = models.DateField()
    #estado
    def __str__(self):
        return str(self.numero)


class DetalleRemitoVencido(models.Model):
    numeroRemito = models.ForeignKey('RemitoMedVencido', on_delete=models.CASCADE)
    cantidad = models.BigIntegerField()
    #estado

    def __str__(self):
        return str(self.numero)

#CLASE ABSTRACTA PEDIDO VENTA
class PedidoVenta(models.Model):
    FILTROS = "farmacia__razonSocial__icontains"
    nroPedido = models.AutoField(primary_key=True)
    fecha = models.DateField(editable=True)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.nroPedido)


#CLASE ABSTRACTA DETALLE PEDIDO
class DetallePedido(models.Model):
    cantidad = models.PositiveIntegerField()
    medicamento = models.ForeignKey('medicamentos.Medicamento')

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.id)

#PEDIDO DE FARMACIA
class PedidoFarmacia(PedidoVenta):
    FILTROS = ["farmacia", "desde", "hasta"]
    FILTERMAPPER = {
        'desde': "fecha__gte",
        'hasta': "fecha__lte",
        'farmacia': "farmacia__razonSocial__icontains"
    }
    ESTADOS = (
        ('Pendiente', 'Pendiente'),
        ('Parcialmente enviado', 'Parcialmente enviado'),
        ('Enviado', 'Enviado'),
    )
    farmacia = models.ForeignKey('organizaciones.Farmacia')
    estado = models.CharField(max_length=25, choices=ESTADOS)

    class Meta(PedidoVenta.Meta):
        verbose_name_plural = "Pedidos de Farmacia"



#DETALLE PEDIDO DE FARMACIA

class DetallePedidoFarmacia(DetallePedido):
    pedidoFarmacia = models.ForeignKey('PedidoFarmacia')
    cantidadPendiente =models.PositiveIntegerField(default= 0)
    estaPedido = models.BooleanField(default= False)


    class Meta(DetallePedido.Meta):
        verbose_name_plural = "Detalles de Pedidos de Farmacia"
















