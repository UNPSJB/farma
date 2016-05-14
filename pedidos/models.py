from django.db import models
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from pedidos import config


# ******************CLASES ABSTRACTAS******************#

class PedidoVenta(models.Model):
    FILTROS = "farmacia__razonSocial__icontains"
    nroPedido = models.AutoField(primary_key=True)
    fecha = models.DateField()

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.nroPedido)


class DetallePedidoVenta(models.Model):
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1), 
                                           MaxValueValidator(config.MAXIMA_CANTIDAD_MEDICAMENTOS)])
    medicamento = models.ForeignKey('medicamentos.Medicamento')

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.id)


# ******************REMITOS Y DETALLES REMITOS DE FARMACIA******************#

class RemitoDeFarmacia(models.Model):
    pedidoFarmacia = models.ForeignKey('PedidoDeFarmacia', on_delete=models.CASCADE)
    fecha = models.DateField()

    def __str__(self):
        return str(self.id)

    def to_json(self):
        if self.pk:
            return {
                'nroRemito': self.pk,
                'fecha': self.fecha
            }


class DetalleRemitoDeFarmacia(models.Model):
    remito = models.ForeignKey(RemitoDeFarmacia, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    detallePedidoDeFarmacia = models.ForeignKey('DetallePedidoDeFarmacia', on_delete=models.CASCADE)
    lote = models.ForeignKey('medicamentos.Lote')

    def __str__(self):
        return str(self.id)

    def set_detalle_pedido(self, detalle):
        self.detallePedidoDeFarmacia = detalle


# ******************REMITO Y DETALLES REMITO DE PEDIDO DE CLINICA******************#

class RemitoDeClinica(models.Model):
    pedidoDeClinica = models.ForeignKey('PedidoDeClinica', on_delete=models.CASCADE)
    fecha = models.DateField()

    def __str__(self):
        return str(self.id)

    def set_pedido(self, pedido):
        self.pedidoDeClinica = pedido

    def to_json(self):
        if self.pk:
            return {
                'nroRemito': self.pk,
                'fecha': self.fecha
            }


class DetalleRemitoDeClinica(models.Model):
    remito = models.ForeignKey('RemitoDeClinica', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    detallePedidoDeClinica = models.ForeignKey('DetallePedidoDeClinica', on_delete=models.CASCADE)
    lote = models.ForeignKey('medicamentos.Lote')

    def __str__(self):
        return str(self.id)

    def set_detalle_pedido(self, detalle):
        self.detallePedidoDeClinica = detalle


# ******************REMITO Y DETALLES REMITO DE DEVOLUCION DE MEDICAMENTOS VENCIDOS******************#

class RemitoMedicamentosVencidos(models.Model):
    numero = models.BigIntegerField()
    fecha = models.DateField()
    laboratorio = models.ForeignKey('organizaciones.Laboratorio', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.numero)

    def to_json(self):
        if self.laboratorio:
            return {'laboratorio': {'id': self.laboratorio.id,
                                 'razonSocial': self.laboratorio.razonSocial},
                    'fecha': datetime.datetime.now().strftime('%d/%m/%Y')}
        else:
            return {}

        
class DetalleRemitoMedicamentosVencido(models.Model):
    remito = models.ForeignKey('RemitoMedicamentosVencidos', on_delete=models.CASCADE)
    medicamento = models.ForeignKey('medicamentos.Medicamento')
    lote = models.ForeignKey('medicamentos.Lote')
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return str(self.id)


# ******************REMITO Y DETALLES REMITO DE LABORATORIO******************#

class RemitoLaboratorio(models.Model):
    nroRemito = models.BigIntegerField(primary_key=True, unique=True)
    fecha = models.DateField()
    laboratorio = models.ForeignKey('organizaciones.Laboratorio', on_delete=models.CASCADE)
    pedidoLaboratorio = models.ForeignKey('PedidoAlaboratorio', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.nroRemito)

    def to_json(self):
        if self.nroRemito:
            return {
                'nroRemito': self.nroRemito,
                'fecha': self.fecha
            }


class DetalleRemitoLaboratorio(models.Model):
    remito = models.ForeignKey('RemitoLaboratorio', on_delete=models.CASCADE)
    lote = models.ForeignKey('medicamentos.Lote')
    detallePedidoLaboratorio = models.ForeignKey('DetallePedidoAlaboratorio')
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return str(self.id)


# ******************PEDIDO DE FARMACIA Y DETALLE PEDIDO DE FARMACIA******************#

class PedidoDeFarmacia(PedidoVenta):
    FILTROS = ["farmacia", "desde", "hasta","estado"]
    FILTERMAPPER = {
        'desde': "fecha__gte",
        'hasta': "fecha__lte",
        'farmacia': "farmacia__razonSocial__icontains",
        'estado': "estado__istartswith"
    }
    farmacia = models.ForeignKey('organizaciones.Farmacia', on_delete=models.CASCADE)
    estado = models.CharField(max_length=25, blank=True)

    class Meta(PedidoVenta.Meta):
        verbose_name_plural = "Pedidos de Farmacia"
        permissions = (
            ("generar_reporte_farmacia", "Puede generar el reporte de pedidos a farmacia"),
        )

    def to_json(self):
        if self.farmacia:
            return {'farmacia': {'id': self.farmacia.id,
                                 'razonSocial': self.farmacia.razonSocial},
                    'fecha': self.fecha.strftime('%d/%m/%Y')}
        else:
            return {}

    def get_detalles(self):
        response = []
        if self.nroPedido:
            response = DetallePedidoDeFarmacia.objects.filter(pedidoDeFarmacia=self)
        return response


class DetallePedidoDeFarmacia(DetallePedidoVenta):
    pedidoDeFarmacia = models.ForeignKey('PedidoDeFarmacia', on_delete=models.CASCADE)
    cantidadPendiente = models.PositiveIntegerField(default=0)
    estaPedido = models.BooleanField(default=False)

    class Meta(DetallePedidoVenta.Meta):
        verbose_name_plural = "Detalles de Pedidos de Farmacia"

    def to_json(self):
        #para evitar acceder a campos nulos
        if self.medicamento:
            return {'medicamento': {"id": self.medicamento.id,
                                    "descripcion": self.medicamento.nombreFantasia.nombreF + " " +
                                                   self.medicamento.presentacion.descripcion + " " +
                                                   str(self.medicamento.presentacion.cantidad) + " " +
                                                   self.medicamento.presentacion.unidadMedida},
                    'cantidad': self.cantidad, 'cantidadPendiente': self.cantidadPendiente}
        else:
            return {}

    def set_pedido(self, pedido):
        self.pedidoDeFarmacia = pedido


# ******************PEDIDO DE CLINICA Y DETALLE PEDIDO DE CLINICA******************#

class PedidoDeClinica(PedidoVenta):
    FILTROS = ["clinica", "obraSocial", "desde", "hasta"]
    FILTERMAPPER = {
        'desde': "fecha__gte",
        'hasta': "fecha__lte",
        'obraSocial': "obraSocial__icontains",
        'clinica': "clinica__razonSocial__icontains"
    }
    clinica = models.ForeignKey('organizaciones.Clinica', on_delete=models.CASCADE)
    obraSocial = models.CharField(max_length=80)
    medicoAuditor = models.CharField(max_length=80)

    class Meta(PedidoVenta.Meta):
        verbose_name_plural = "Pedidos de Clinica"

    def to_json(self):
        if self.clinica:
            return {'clinica': {'id': self.clinica.id,
                                 'razonSocial': self.clinica.razonSocial},
                    'fecha': self.fecha.strftime('%d/%m/%Y'),
                    'obraSocial': self.obraSocial,
                    'medicoAuditor': self.medicoAuditor}
        else:
            return {}

    def get_detalles(self):
        response = []
        if self.nroPedido:
            response = DetallePedidoDeClinica.objects.filter(pedidoDeClinica=self)
        return response


class DetallePedidoDeClinica(DetallePedidoVenta):
    pedidoDeClinica = models.ForeignKey('PedidoDeClinica', on_delete=models.CASCADE)
    cantidadPendiente = models.PositiveIntegerField(default=0)
    estaPedido = models.BooleanField(default=False)

    class Meta(DetallePedidoVenta.Meta):
        verbose_name_plural = "Detalles de Pedidos de Clinica"

    def to_json(self):
        #para evitar acceder a campos nulos
        if self.medicamento:
            return {'medicamento': {"id": self.medicamento.id,
                                    "descripcion": self.medicamento.nombreFantasia.nombreF + " " +
                                                   self.medicamento.presentacion.descripcion + " " +
                                                   str(self.medicamento.presentacion.cantidad) + " " +
                                                   self.medicamento.presentacion.unidadMedida},
                    'cantidad': self.cantidad}
        else:
            return {}

    def set_pedido(self, pedido):
        self.pedidoDeClinica = pedido


# ================================================ PEDIDO A LABORATORIO ================================================

# PEDIDO A LABORATORIO

class PedidoAlaboratorio(models.Model):
    FILTROS = ["laboratorio", "desde", "hasta"]
    FILTERMAPPER = {
        'laboratorio': "laboratorio__razonSocial__icontains",
        'desde': "fecha__gte",
        'hasta': "fecha__lte"
    }
    nroPedido = models.AutoField(primary_key=True)
    fecha = models.DateField(auto_now_add=True)
    laboratorio = models.ForeignKey('organizaciones.Laboratorio', on_delete=models.CASCADE)

    estado = models.CharField(max_length=25, blank=True, default="Pendiente")# cancelado, parcialmente recibido, pendiente, completo

    def __str__(self):
        return 'Pedido Nro %s - Laboratorio: %s' % (self.nroPedido, self.laboratorio)
    
    def to_json(self):
        if self.laboratorio:
            return {'laboratorio': {'id': self.laboratorio.id,
                                 'razonSocial': self.laboratorio.razonSocial},
                    'fecha': datetime.datetime.now().strftime('%d/%m/%Y')}
        else:
            return {}

    def get_detalles(self):
        response = []
        if self.nroPedido:
            response = DetallePedidoAlaboratorio.objects.filter(pedido=self)
        return response


# DETALLE PEDIDO A LABORATORIO

class DetallePedidoAlaboratorio(models.Model):
    renglon = models.AutoField(primary_key=True)
    pedido = models.ForeignKey('PedidoAlaboratorio', null=True, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1), 
                                           MaxValueValidator(config.MAXIMA_CANTIDAD_MEDICAMENTOS)])
    cantidadPendiente = models.PositiveIntegerField()
    medicamento = models.ForeignKey('medicamentos.Medicamento')
    detallePedidoFarmacia = models.ForeignKey('DetallePedidoDeFarmacia', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "Pedido Nro %s - Detalle %s"%(self.pedido.nroPedido, self.renglon)
    
    def to_json(self):
        response = {}

        # para evitar acceder a campos nulos
        if self.renglon:
            response['renglon'] = self.renglon

        # para evitar acceder a campos nulos
        if self.medicamento:
            response['medicamento'] = {"id": self.medicamento.id,
                                       "descripcion": self.medicamento.nombreFantasia.nombreF + " " +
                                                   self.medicamento.presentacion.descripcion + " " +
                                                   str(self.medicamento.presentacion.cantidad) + " " +
                                                   self.medicamento.presentacion.unidadMedida }

        if self.detallePedidoFarmacia:
            response['detallePedidoFarmacia'] = self.detallePedidoFarmacia.pk
        else:
            response['detallePedidoFarmacia'] = -1

        response['cantidad'] = self.cantidad
        response['cantidadPendiente'] = self.cantidadPendiente
        return response