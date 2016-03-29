from django.db import models
import datetime

#******************CLASES ABSTRACTAS******************#

class PedidoVenta(models.Model):
    FILTROS = "farmacia__razonSocial__icontains"
    nroPedido = models.AutoField(primary_key=True)
    fecha = models.DateField()

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.nroPedido)

class DetallePedidoVenta(models.Model):
    cantidad = models.PositiveIntegerField()
    medicamento = models.ForeignKey('medicamentos.Medicamento')

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.id)


#******************REMITOS Y DETALLES REMITOS DE FARMACIA******************#
class RemitoDeFarmacia(models.Model):

    pedidoFarmacia = models.ForeignKey('PedidoDeFarmacia', on_delete=models.CASCADE)
    fecha = models.DateField()

    def __str__(self):
        return str(self.id)

class DetalleRemitoDeFarmacia(models.Model):

    remito = models.ForeignKey(RemitoDeFarmacia, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    detallePedidoDeFarmacia = models.ForeignKey('DetallePedidoDeFarmacia')
    lote = models.ForeignKey('medicamentos.Lote')

    def __str__(self):
        return str(self.id)

    def set_detalle_pedido(self, detalle):
        self.detallePedidoDeFarmacia = detalle

#******************REMITO Y DETALLES REMITO DE PEDIDO DE CLINICA******************#

class RemitoDeClinica(models.Model):

    pedidoDeClinica = models.ForeignKey('PedidoDeClinica', on_delete=models.CASCADE)
    fecha = models.DateField()

    def __str__(self):
        return str(self.id)

    def set_pedido(self, pedido):
        self.pedidoDeClinica = pedido

class DetalleRemitoDeClinica(models.Model):

    remito = models.ForeignKey('RemitoDeClinica', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    detallePedidoDeClinica = models.ForeignKey('DetallePedidoDeClinica')
    lote = models.ForeignKey('medicamentos.Lote')

    def __str__(self):
        return str(self.id)

    def set_detalle_pedido(self, detalle):
        self.detallePedidoDeClinica = detalle


#******************REMITO Y DETALLES REMITO DE DEVOLUCION DE MEDICAMENTOS VENCIDOS******************#

class RemitoMedicamentosVencidos(models.Model):
    numero = models.BigIntegerField()
    fecha = models.DateField()
    laboratorio = models.ForeignKey('organizaciones.Laboratorio')

    def __str__(self):
        return str(self.numero)
        
class DetalleRemitoMedicamentosVencido(models.Model):
    remito = models.ForeignKey('RemitoMedicamentosVencidos', on_delete=models.CASCADE)
    lote = models.ForeignKey('medicamentos.Lote')
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return str(self.numero)


#******************PEDIDO DE FARMACIA Y DETALLE PEDIDO DE FARMACIA******************#

class PedidoDeFarmacia(PedidoVenta):

    FILTROS = ["farmacia", "desde", "hasta","estado"]
    FILTERMAPPER = {
        'desde': "fecha__gte",
        'hasta': "fecha__lte",
        'farmacia': "farmacia__razonSocial__icontains",
        'estado': "estado__icontains"
    }
    farmacia = models.ForeignKey('organizaciones.Farmacia')
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
    pedidoDeFarmacia = models.ForeignKey('PedidoDeFarmacia')
    cantidadPendiente =models.PositiveIntegerField(default= 0)
    estaPedido = models.BooleanField(default= False)


    class Meta(DetallePedidoVenta.Meta):
        verbose_name_plural = "Detalles de Pedidos de Farmacia"

    def to_json(self):
        #para evitar acceder a campos nulos
        if self.medicamento:
            return {'medicamento': {"id": self.medicamento.id,
                                    "descripcion": self.medicamento.nombreFantasia.nombreF + " " +
                                                   self.medicamento.presentacion.descripcion + " " +
                                                   str(self.medicamento.presentacion.cantidad) + " " +
                                                   self.medicamento.presentacion.unidadMedida },
                    'cantidad': self.cantidad, 'cantidadPendiente': self.cantidadPendiente}
        else:
            return {}

    def set_pedido(self, pedido):
        self.pedidoDeFarmacia = pedido

#******************PEDIDO DE CLINICA Y DETALLE PEDIDO DE CLINICA******************#

class PedidoDeClinica(PedidoVenta):

    FILTROS = ["clinica", "desde", "hasta"]
    FILTERMAPPER = {
        'desde': "fecha__gte",
        'hasta': "fecha__lte",
        'clinica': "clinica__razonSocial__icontains"
    }
    clinica = models.ForeignKey('organizaciones.Clinica')
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
    pedidoDeClinica = models.ForeignKey('PedidoDeClinica')
    cantidadPendiente =models.PositiveIntegerField(default= 0)
    estaPedido = models.BooleanField(default= False)


    class Meta(DetallePedidoVenta.Meta):
        verbose_name_plural = "Detalles de Pedidos de Clinica"

    def to_json(self):
        #para evitar acceder a campos nulos
        if self.medicamento:
            return {'medicamento': {"id": self.medicamento.id,
                                    "descripcion": self.medicamento.nombreFantasia.nombreF + " " +
                                                   self.medicamento.presentacion.descripcion + " " +
                                                   str(self.medicamento.presentacion.cantidad) + " " +
                                                   self.medicamento.presentacion.unidadMedida },
                    'cantidad': self.cantidad}
        else:
            return {}

    def set_pedido(self, pedido):
        self.pedidoDeClinica = pedido

#================================================PEDIDO A LABORATORIO===================================================

#PEDIDO A LABORATORIO

class PedidoAlaboratorio(models.Model):
    FILTROS = ["laboratorio"]
    FILTERMAPPER = {
        'laboratorio': "laboratorio__razonSocial__icontains"
    }
    numero = models.AutoField(primary_key=True)
    fecha = models.DateField(auto_now_add=True)
    laboratorio = models.ForeignKey('organizaciones.Laboratorio')

    estado = models.CharField(max_length=25, blank=True, default="Pendiente")#cancelado, parcialmente recibido, pendiente, completo

    def __str__(self):
        return 'Pedido Nro %s - Laboratorio: %s' % (self.numero, self.laboratorio)
    
    def to_json(self):
        if self.laboratorio:
            return {'laboratorio': {'id': self.laboratorio.id,
                                 'razonSocial': self.laboratorio.razonSocial},
                    'fecha': datetime.datetime.now().strftime('%d/%m/%Y')}
        else:
            return {}

#DETALLE PEDIDO A LABORATORIO

class DetallePedidoAlaboratorio(models.Model):
    renglon = models.AutoField(primary_key=True)
    pedido = models.ForeignKey('PedidoAlaboratorio', null=True)
    cantidad = models.PositiveIntegerField()
    cantidadPendiente = models.PositiveIntegerField()
    medicamento = models.ForeignKey('medicamentos.Medicamento')
    detallePedidoFarmacia = models.ForeignKey('DetallePedidoDeFarmacia', blank=True, null=True)
    
    def __str__(self):
        return "Pedido Nro %s - Detalle %s"%(self.pedido.numero, self.renglon)
    
    def to_json(self):
        response = {}

        #para evitar acceder a campos nulos
        if self.renglon:
            response['renglon'] = self.renglon

        #para evitar acceder a campos nulos
        if self.medicamento:
            response['medicamento'] = {"id": self.medicamento.id,
                                       "descripcion": self.medicamento.nombreFantasia.nombreF + " " +
                                                   self.medicamento.presentacion.descripcion + " " +
                                                   str(self.medicamento.presentacion.cantidad) + " " +
                                                   self.medicamento.presentacion.unidadMedida }

        response['cantidad'] = self.cantidad
        response['cantidadPendiente'] = self.cantidadPendiente
        return response