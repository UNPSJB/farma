from pedidos import models
from medicamentos.models import Lote

def get_stock_total(medicamento):
    lotes = Lote.objects.filter(medicamento__id=medicamento.id)
    stockTotal = 0
    for lote in lotes:
        stockTotal += lote.stock
    return stockTotal


""" Funcion que procesa el detalle del pedido de farmacia recibido por parametro.
Se encarga de crear o no, el o los correspondientes detalles en el remito y asociarlos
al detalle del pedido(recibido por parametro).
PRE: * detalle -> detalle del pedido de farmacia.
     * remito  -> remito que apunta al pedido que contiene el detalle recibido.
POS: * Retorna True si hubo suficiente stock para satisfacer la cantidad del medicamento solicitada en el detalle.
     * Retorna False si no hay stock suficiente(o directamente no hay) para satisfacer la cantidad del medicamento
       solicitada en el detalle.
     * detalle del pedido y lotes utilizados estan actualizados.
     * Cero o mas detalles de remito creados. """

def procesar_detalle(detalle, remito):
    stockTotal = get_stock_total(detalle.medicamento)
    lotes = Lote.objects.filter(medicamento__id=detalle.medicamento.id).order_by('fechaVencimiento')
    if stockTotal < detalle.cantidad:
        for lote in lotes:
            if lote.stock:  # Solo uso lotes que no esten vacios
                cantidadTomadaDeLote = lote.stock
                lote.stock = 0
                detalleRemito = models.DetalleRemitoPedidoDeFarmacia() if isinstance(remito, models.RemitoPedidoDeFarmacia) else models.DetalleRemitoPedidoDeClinica()
                detalleRemito.remito = remito
                detalleRemito.set_detalle_pedido(detalle)
                detalleRemito.lote = lote
                detalleRemito.cantidad = cantidadTomadaDeLote

                detalleRemito.save()
                lote.save()

        detalle.cantidadPendiente = detalle.cantidad-stockTotal
        detalle.save()
        return False
    else:
        detalle.cantidadPendiente = 0  # porque hay stock suficiente para el medicamento del detalle
        detalle.save()  # actualizo cantidad pendiente antes calculada
        cantidadNecesaria = detalle.cantidad
        i = 0
        while cantidadNecesaria > 0:
            lote = lotes[i]
            if lote.stock:  # Solo uso lotes que no esten vacios
                cantidadTomadaDeLote = 0
                if lote.stock < cantidadNecesaria:  # el lote no tiene toda la cantidad que necesito
                    cantidadNecesaria -= lote.stock
                    cantidadTomadaDeLote = lote.stock
                    lote.stock = 0
                else:
                    lote.stock = lote.stock - cantidadNecesaria
                    cantidadTomadaDeLote = cantidadNecesaria
                    cantidadNecesaria = 0

                detalleRemito = models.DetalleRemitoPedidoDeFarmacia() if isinstance(remito, models.RemitoPedidoDeFarmacia) else models.DetalleRemitoPedidoDeClinica()
                detalleRemito.remito = remito
                detalleRemito.set_detalle_pedido(detalle)
                detalleRemito.lote = lote
                detalleRemito.cantidad = cantidadTomadaDeLote
                detalleRemito.save()
                lote.save()  # actualizo el stock del lote
            i += 1
        return True



def es_pendiente(pedido):
    detalles = pedido.get_detalles()
    for detalle in detalles:
        if get_stock_total(detalle.medicamento) > 0:
            return False
    return True


def procesar_pedido_de_farmacia(pedido):
    detalles = pedido.get_detalles()
    if not es_pendiente(pedido):
        remito = models.RemitoPedidoDeFarmacia()
        remito.fecha = pedido.fecha
        remito.set_pedido(pedido)
        remito.save()
        esEnviado = True
        for detalle in detalles:
            resp = procesar_detalle(detalle, remito)
            esEnviado = esEnviado and resp

        pedido.estado = "Enviado" if esEnviado else "Parcialmente Enviado"
    else:
        pedido.estado = "Pendiente"
        for detalle in detalles:
            detalle.cantidadPendiente = detalle.cantidad
            detalle.save()
    pedido.save()

def procesar_pedido_de_clinica(pedido):
    detalles = pedido.get_detalles()
    if not es_pendiente(pedido):
        remito = models.RemitoPedidoDeClinica()
        remito.fecha = pedido.fecha
        remito.set_pedido(pedido)
        remito.save()
        for detalle in detalles:
            procesar_detalle(detalle, remito)
