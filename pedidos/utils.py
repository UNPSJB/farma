from pedidos import models
from medicamentos.models import Lote

def get_stock_total(lotes):
    stockTotal = 0
    for lote in lotes:
        stockTotal += lote.stock

    return stockTotal


def procesar_detalle(detallePedidoFarmacia):
    lotes = Lote.objects.filter(medicamento__id=detallePedidoFarmacia.medicamento.id).order_by('fechaVencimiento')
    stockTotal = get_stock_total(lotes)
    if stockTotal == 0:
        print "Stock cero"
        detallePedidoFarmacia.cantidadPendiente=detallePedidoFarmacia.cantidad
        detallePedidoFarmacia.save()
    else:
        remito = models.Remito.objects.get(pedidoFarmacia__nroPedido=detallePedidoFarmacia.pedidoFarmacia.nroPedido)

        if stockTotal < detallePedidoFarmacia.cantidad:
            print "Stock insuficiente"
            cantidadTotal=0

            for lote in lotes:
                cantidadTotal += lote.stock
                cantidadTomadaDeLote = lote.stock
                lote.stock = 0
                detalleRemito = models.DetalleRemito()
                detalleRemito.remito = remito
                detalleRemito.detallePedidoFarmacia = detallePedidoFarmacia
                detalleRemito.lote = lote
                detalleRemito.cantidad = cantidadTomadaDeLote

                detalleRemito.save()
                lote.save()

            #Vuelvo a guardar el detalle del pedido con la cantidad pendiente
            detallePedidoFarmacia.cantidadPendiente=detallePedidoFarmacia.cantidad-cantidadTotal
            detallePedidoFarmacia.save()
        else:
            print "stock suficiente"
            detallePedidoFarmacia.cantidadPendiente=0
            cantidadNecesaria = detallePedidoFarmacia.cantidad
            detallePedidoFarmacia.save()
            i = 0
            while cantidadNecesaria > 0:
                lote = lotes[i]
                cantidadTomadaDeLote = 0
                if lote.stock < cantidadNecesaria:
                    cantidadNecesaria -= lote.stock
                    cantidadTomadaDeLote = lote.stock
                    lote.stock = 0
                else:
                    lote.stock -= cantidadNecesaria
                    cantidadTomadaDeLote = cantidadNecesaria
                    cantidadNecesaria = 0

                detalleRemito = models.DetalleRemito()
                detalleRemito.remito = remito
                detalleRemito.detallePedidoFarmacia = detallePedidoFarmacia
                detalleRemito.lote = lote
                detalleRemito.cantidad = cantidadTomadaDeLote

                detalleRemito.save()
                lote.save()

                i += 1


def setearEstado(id_pedido):

    pedido= models.PedidoFarmacia.objects.get(id_pedido)
    detallesPedido = models.DetallePedidoFarmacia.objects.filter(pedidoFarmacia__nroPedido = id_pedido)
    remito = models.Remito.objects.get(pedidoFarmacia__nroPedido = id_pedido)
    detalleRemito = models.DetalleRemito.objects.filter(remito__id = remito.id)


    if (not(detalleRemito)):
        pedido.estado = "Pendiente"
        remito.delete()
    else:

        for detalle in detallesPedido:
            if(detalle.cantidadPendiente <> 0):
                pedido.estado = "Parcialmente Enviado"
                break

    pedido.save()
