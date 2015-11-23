from django.db import models

# Create your models here.

class Remito(models.Model):
    pedidoFarmacia = models.ForeignKey('PedidoDeFarmacia', on_delete=models.CASCADE)
    fecha = models.DateField()

    def __str__(self):
        return str(self.id)

class DetalleRemito(models.Model):
    remito = models.ForeignKey(Remito, on_delete=models.CASCADE)
    cantidad = models.BigIntegerField()
    detallePedidoFarmacia = models.ForeignKey('DetallePedidoDeFarmacia')
    lote = models.ForeignKey('medicamentos.Lote')

    def __str__(self):
        return str(self.id)

class RemitoMedicamentosVencido(models.Model):
    numero = models.BigIntegerField()
    fecha = models.DateField()

    def __str__(self):
        return str(self.numero)


class DetalleRemitoMedicamentosVencido(models.Model):
    remito = models.ForeignKey('RemitoMedicamentosVencido', on_delete=models.CASCADE)
    cantidad = models.BigIntegerField()


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
class DetallePedidoVenta(models.Model):
    cantidad = models.PositiveIntegerField()
    medicamento = models.ForeignKey('medicamentos.Medicamento')

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.id)

#PEDIDO DE FARMACIA
class PedidoDeFarmacia(PedidoVenta):

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
        permissions = (
            ("generar_reporte_farmacia", "Puede generar el reporte de pedidos a farmacia"),
        )


#DETALLE PEDIDO DE FARMACIA

class DetallePedidoDeFarmacia(DetallePedidoVenta):
    pedidoFarmacia = models.ForeignKey('PedidoDeFarmacia')
    cantidadPendiente =models.PositiveIntegerField(default= 0)
    estaPedido = models.BooleanField(default= False)


    class Meta(DetallePedidoVenta.Meta):
        verbose_name_plural = "Detalles de Pedidos de Farmacia"


