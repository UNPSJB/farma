from pedidos import models
from medicamentos.models import Lote

def get_stock_total(lotes):
    stockTotal = 0
    for lote in lotes:
        stockTotal += lote.stock

    return stockTotal


def procesar_detalle(detallePedidoFarmacia, remito):
    lotes = Lote.objects.filter(medicamento__id=detallePedidoFarmacia.medicamento.id).order_by('fechaVencimiento')
    stockTotal = get_stock_total(lotes)
    if stockTotal == 0:
        print "Stock cero"
        detallePedidoFarmacia.cantidadPendiente=detallePedidoFarmacia.cantidad
        detallePedidoFarmacia.save()
    else:


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



def procesarPedido(pedido):

    detallesPedido = models.DetallePedidoDeFarmacia.objects.filter(pedidoFarmacia__nroPedido = pedido.nroPedido)

    creaRemito = False

    for detalle in detallesPedido:

        lotes = Lote.objects.filter(medicamento__id=detalle.medicamento.id).order_by('fechaVencimiento')
        stockTotal = get_stock_total(lotes)
        print stockTotal
        if (stockTotal <> 0 ):
            creaRemito = True
            break


    if(creaRemito):

        remitoNuevo = models.Remito(pedidoFarmacia = pedido, fecha=pedido.fecha)
        remitoNuevo.save()

        for detalle in detallesPedido:

            procesar_detalle(detalle, remitoNuevo)

        detallesRemito= models.DetalleRemito.objects.filter(remito__id = remitoNuevo.id)

        if(detallesRemito):
            for detalle in detallesPedido:
                if(detalle.cantidadPendiente <>0):
                    pedido.estado = "Parcialmente Enviado"
                    break

    else:
        pedido.estado= "Pendiente"


    pedido.save()




