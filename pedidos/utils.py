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
        pass
    else:
        remito = models.Remito.objects.get(pedidoFarmacia__nroPedido=detallePedidoFarmacia.pedidoFarmacia.nroPedido)

        if stockTotal < detallePedidoFarmacia.cantidad:
            print "Stock insuficiente"
            for lote in lotes:
                detallePedidoFarmacia.cantidad -= lote.stock
                cantidadTomadaDeLote = lote.stock
                lote.stock = 0
                detalleRemito = models.DetalleRemito()
                detalleRemito.remito = remito
                detalleRemito.detallePedidoFarmacia = detallePedidoFarmacia
                detalleRemito.lote = lote
                detalleRemito.cantidad = cantidadTomadaDeLote

                detalleRemito.save()
                lote.save()

            #Vuelvo a guardar el detalle del pedido con la nueva cantidad
            detallePedidoFarmacia.save()
        else:
            print "stock suficiente"
            cantidadNecesaria = detallePedidoFarmacia.cantidad
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
