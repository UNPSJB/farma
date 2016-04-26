#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db.models import Q

import datetime
import re

from medicamentos import models as mmodels
from organizaciones import models as omodels
from pedidos import models


#**********************
# FUNCIONES COMPARTIDAS
#**********************
def crear_pedido_para_sesion(m, pedido):
    p = pedido.to_json()
    p['nroPedido'] = get_next_nro_pedido(m)
    return p

def get_next_nro_pedido(m):
    nro = 1
    try:
        nro = m.objects.latest('nroPedido').nroPedido + 1
    except m.DoesNotExist:
        pass
    return nro

def existe_medicamento_en_pedido(detalles, id_med):
    for detalle in detalles:
        if detalle['medicamento']['id'] == id_med: #no puede haber dos detalles con el mismo medicamento
            return True
    return False

def crear_detalle_json(detalle, renglon):
    d = detalle.to_json()
    d['renglon'] = renglon
    return d

#**********************
# PEDIDO DE FARMACIA
#**********************

def procesar_pedido_de_farmacia(pedido):
    detalles = models.DetallePedidoDeFarmacia.objects.filter(pedidoDeFarmacia=pedido.nroPedido) #obtengo todos los detalles del pedido
    if not es_pendiente(pedido):
        remito = models.RemitoDeFarmacia(pedidoFarmacia=pedido, fecha=pedido.fecha)
        remito.save()
        esEnviado = True
        for detalle in detalles:
            esEnviado = esEnviado and procesar_detalle_de_farmacia(detalle, remito)

        pedido.estado = "Enviado" if esEnviado else "Parcialmente Enviado"
    else:
        pedido.estado = "Pendiente"
        for detalle in detalles:
            detalle.cantidadPendiente = detalle.cantidad
            detalle.save()
    pedido.save()

"""FUNCIONES INTERNAS PEDIDO DE FARMACIA"""

def procesar_detalle_de_farmacia(detalle, remito):
    stockTotal = detalle.medicamento.get_stock()
    lotes = mmodels.Lote.objects.filter(medicamento__id=detalle.medicamento.id).order_by('fechaVencimiento')
    if stockTotal < detalle.cantidad:
        for lote in lotes:
            if lote.stock:  # Solo uso lotes que no esten vacios
                cantidadTomadaDeLote = lote.stock
                lote.stock = 0
                detalleRemito = models.DetalleRemitoDeFarmacia()
                detalleRemito.remito = remito
                detalleRemito.set_detalle_pedido(detalle)
                detalleRemito.lote = lote
                detalleRemito.cantidad = cantidadTomadaDeLote
                detalleRemito.detallePedidoDeFarmacia = detalle
                detalleRemito.lote = lote
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

                detalleRemito = models.DetalleRemitoDeFarmacia()
                detalleRemito.remito = remito
                detalleRemito.detallePedidoDeFarmacia = detalle
                detalleRemito.lote = lote
                detalleRemito.cantidad = cantidadTomadaDeLote
                detalleRemito.save()
                lote.save()  # actualizo el stock del lote
            i += 1
        return True

def es_pendiente(pedido):
    detalles = models.DetallePedidoDeFarmacia.objects.filter(pedidoDeFarmacia=pedido.nroPedido) #obtengo todos los detalles del pedido
    for detalle in detalles:
        if detalle.medicamento.get_stock() > 0:
            return False
    return True



#**********************
# PEDIDO DE CLINICA
#**********************

def get_medicamentos_con_stock():
    medicamentos_con_stock = []
    medicamentos = mmodels.Medicamento.objects.all()
    for medicamento in medicamentos:
        lotes = mmodels.Lote.objects.filter(medicamento=medicamento)
        if lotes.count() > 0:
            hayStock = False
            for lote in lotes:
                if lote.stock > 0:
                    hayStock = True
                    break
            if hayStock:
                medicamentos_con_stock.append(medicamento.id)
    return mmodels.Medicamento.objects.filter(pk__in=medicamentos_con_stock)

def procesar_pedido_de_clinica(pedido):
    detalles = models.DetallePedidoDeClinica.objects.filter(pedidoDeClinica=pedido.nroPedido) #obtengo todos los detalles del pedido
    remito = models.RemitoDeClinica(pedidoDeClinica=pedido, fecha=pedido.fecha)
    remito.save()
    for detalle in detalles:
        procesar_detalle_de_clinica(detalle, remito)

"""FUNCIONES INTERNAS PEDIDO DE CLINICA"""

def procesar_detalle_de_clinica(detalle, remito):
    lotes = mmodels.Lote.objects.filter(medicamento__id=detalle.medicamento.id).order_by('fechaVencimiento')
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

            detalleRemito = models.DetalleRemitoDeClinica()
            detalleRemito.remito = remito
            detalleRemito.detallePedidoDeClinica = detalle
            detalleRemito.lote = lote
            detalleRemito.cantidad = cantidadTomadaDeLote
            detalleRemito.save()
            lote.save()  # actualizo el stock del lote
        i += 1





#**********************
# PEDIDO A LABORATORIO
#**********************

def get_next_nro_pedido_laboratorio(m, nombrePk):
    nro = None
    try:
        nro = m.objects.latest(nombrePk).numero + 1
    except m.DoesNotExist:
        nro = 1
    return nro

def get_detalles_a_pedir(pkLaboratorio):
    detalles_a_pedir = []
    pedidos = models.PedidoDeFarmacia.objects.filter(Q(estado='Pendiente') | Q(estado='Parcialmente Enviado'))
    
    for pedido in pedidos:
        detalles = models.DetallePedidoDeFarmacia.objects.filter(Q(pedidoDeFarmacia=pedido.pk) & Q(estaPedido=False) & Q(cantidadPendiente__gt=0) & Q(medicamento__laboratorio=pkLaboratorio))
        for detalle in detalles:
            # creo el detalle del pedido a laboratorio asociado al detalle pedido de farmacia
            detallePedidoAlaboratorio = models.DetallePedidoAlaboratorio()
            detallePedidoAlaboratorio.medicamento = detalle.medicamento
            detallePedidoAlaboratorio.cantidad = detalle.cantidadPendiente 
            detallePedidoAlaboratorio_json = crear_detalle_json(detallePedidoAlaboratorio, len(detalles_a_pedir) + 1)
            detallePedidoAlaboratorio_json['detallePedidoFarmacia'] = detalle.id
            detalles_a_pedir.append(detallePedidoAlaboratorio_json)
    return detalles_a_pedir


def cancelar_pedido_a_laboratorio(pedido):
    if pedido.estado == "Pendiente":
        detallesPedidoAlaboratorio = models.DetallePedidoAlaboratorio.objects.filter(pedido=pedido)
        for detallePedidoAlaboratorio in detallesPedidoAlaboratorio:
            detallePedidoDeFarmacia = detallePedidoAlaboratorio.detallePedidoFarmacia
            if(detallePedidoDeFarmacia):
                detallePedidoDeFarmacia.estaPedido = False
                detallePedidoDeFarmacia.save()
        pedido.estado = "Cancelado"
        pedido.save()

def existe_medicamento_en_detalle_suelto(detalles, id_medicamento):
    for detalle in detalles:
        if detalle['detallePedidoFarmacia'] == -1 and detalle['medicamento']['id'] == id_medicamento:
            return True
    return False







#*******************************
# RECEPCION PEDIDO A LABORATORIO
#*******************************


def cargar_detalles(id_pedido, session):
    detalles = models.DetallePedidoAlaboratorio.objects.filter(pedido=id_pedido, cantidadPendiente__gt=0)
    recepcionPedidoAlaboratorio = {}
    recepcionPedidoAlaboratorio['nuevosLotes'] = {}
    recepcionPedidoAlaboratorio['actualizarLotes'] = {}
    recepcionPedidoAlaboratorio['detalles'] = []

    for detalle in detalles:
        infoDetalle = detalle.to_json()
        infoDetalle['actualizado'] = False #cuando se actualize el detalle este campo es True
        recepcionPedidoAlaboratorio['detalles'].append(infoDetalle)

    session['recepcionPedidoAlaboratorio'] = recepcionPedidoAlaboratorio


def medicamento_tiene_lotes(medicamento, lotesSesion):
    if mmodels.Lote.objects.filter(medicamento=medicamento).count() > 0:
        return True
    for numeroLote, infoLote in lotesSesion.items():
        if infoLote['medicamento'] == medicamento.id:
            return True
    return False


def hay_cantidad_pendiente(detalles, id_detalle):
    posDetalle = get_pos_detalle(detalles, id_detalle)
    detalle = detalles[posDetalle]
    return detalle['cantidadPendiente'] > 0


def get_pos_detalle(detalles, id_detalle):
    i = 0
    for detalle in detalles:
        if detalle['renglon'] == int(id_detalle):
            return i
        i += 1
    return -1


def guardar_recepcion_detalle(session, detalle, infoRecepcionDetalle):
    recepcionPedidoAlaboratorio = session['recepcionPedidoAlaboratorio']
    detallesRemitoRecepcion= session['remitoRecepcion']['detalles']
    detalles = recepcionPedidoAlaboratorio['detalles']
    posDetalle = get_pos_detalle(detalles, detalle.renglon)
    infoDetalle = detalles[posDetalle]
    numeroLote = str(infoRecepcionDetalle['lote'])
    #informacion del detalle de remito
    detallesRemitoRecepcion.append({'detallePedidoLaboratorio':detalle.pk,'lote':numeroLote,'cantidad':infoRecepcionDetalle['cantidad']})
    session['remitoRecepcion']['detalles']=detallesRemitoRecepcion

    cantidadStockLote = 0
    if infoDetalle['detallePedidoFarmacia'] == -1:
        cantidadStockLote = infoRecepcionDetalle['cantidad']

    if numeroLote in recepcionPedidoAlaboratorio['nuevosLotes']:
        lote = recepcionPedidoAlaboratorio['nuevosLotes'][numeroLote]
        lote['stock'] += cantidadStockLote
        recepcionPedidoAlaboratorio['nuevosLotes'][numeroLote] = lote # guardo cambios
    else:
        if numeroLote in recepcionPedidoAlaboratorio['actualizarLotes']:
            stock = recepcionPedidoAlaboratorio['actualizarLotes'][numeroLote]
            stock += cantidadStockLote
            recepcionPedidoAlaboratorio['actualizarLotes'][numeroLote] = stock # guardo cambios
        else:
            recepcionPedidoAlaboratorio['actualizarLotes'][numeroLote] = cantidadStockLote

    infoDetalle['cantidadPendiente'] -= infoRecepcionDetalle['cantidad']
    infoDetalle['actualizado'] = True
    
    detalles[posDetalle] = infoDetalle # guardo cambios
    recepcionPedidoAlaboratorio['detalles'] = detalles # guardo cambios

    session['recepcionPedidoAlaboratorio'] = recepcionPedidoAlaboratorio # guardo todos los cambios


def guardar_recepcion_detalle_con_nuevo_lote(session, detalle, infoRecepcionDetalle):
    recepcionPedidoAlaboratorio = session['recepcionPedidoAlaboratorio']
    detalles = recepcionPedidoAlaboratorio['detalles']
    detallesRemitoRecepcion = session['remitoRecepcion']['detalles']
    posDetalle = get_pos_detalle(detalles, detalle.renglon)
    infoDetalle = detalles[posDetalle]

    numeroLote = infoRecepcionDetalle['lote']
    cantidadStockLote = 0
    if infoDetalle['detallePedidoFarmacia'] == -1:
        cantidadStockLote = infoRecepcionDetalle['cantidad']
    nuevoLote = {
        'fechaVencimiento': infoRecepcionDetalle['fechaVencimiento'].strftime('%d/%m/%Y'),
        'precio': infoRecepcionDetalle['precio'],
        'stock': cantidadStockLote,
        'medicamento': detalle.medicamento.id
    }  

    recepcionPedidoAlaboratorio['nuevosLotes'][numeroLote] = nuevoLote

    infoDetalle['cantidadPendiente'] -= infoRecepcionDetalle['cantidad']
    infoDetalle['actualizado'] = True
    detalles[posDetalle] = infoDetalle

    recepcionPedidoAlaboratorio['detalles'] = detalles

    session['recepcionPedidoAlaboratorio'] = recepcionPedidoAlaboratorio

    detallesRemitoRecepcion.append({'detallePedidoLaboratorio': detalle.pk, 'lote': numeroLote, 'cantidad': infoRecepcionDetalle['cantidad']})
    session['remitoRecepcion']['detalles'] = detallesRemitoRecepcion


def crear_nuevos_lotes(nuevosLotes):
    for numeroLote, info in nuevosLotes.items():
        lote = mmodels.Lote()
        lote.numero = numeroLote
        lote.fechaVencimiento = datetime.datetime.strptime(info['fechaVencimiento'], '%d/%m/%Y').date()
        lote.precio = info['precio']
        lote.stock = info['stock']
        lote.medicamento = mmodels.Medicamento.objects.get(pk=info['medicamento'])
        lote.save()        

def actualizar_lotes(lotes):
    for numeroLote, cantidadRecibida in lotes.items():
        if cantidadRecibida > 0:
            lote = mmodels.Lote.objects.get(numero=numeroLote)
            lote.stock += cantidadRecibida
            lote.save()

def actualizar_pedido(pedido, detalles):
    recepcionDelPedidoCompleta = True
    for detalle in detalles:
        if detalle['actualizado']:
            detalleDb = models.DetallePedidoAlaboratorio.objects.get(pk=detalle['renglon'])
            detalleDb.cantidadPendiente = detalle['cantidadPendiente']
            if detalleDb.cantidadPendiente > 0:
                recepcionDelPedidoCompleta = False # xq hay al menos un detalle que aún falta satisfacer
            detalleDb.save()
        else:
            recepcionDelPedidoCompleta = False # xq hay al menos un detalle que no acusó ningún tipo de recibo

    if recepcionDelPedidoCompleta:
        pedido.estado = "Completo"
    else:
        pedido.estado = "Parcialmente Recibido"
    pedido.save()


def actualizar_pedidos_farmacia(remitoLab):

    detalles = models.DetalleRemitoLaboratorio.objects.filter(remito=remitoLab)
    #todos los pedidos de farmacia a los que se les realiza el remito y que luego deben actualizar su estado
    listaPedidosDeFarmacia = []

    remitosDeFarmacia = {}
    for detalle in detalles:
        detallePedidoFarmacia = detalle.detallePedidoLaboratorio.detallePedidoFarmacia
        if detallePedidoFarmacia:
            detallesRemito = remitosDeFarmacia.setdefault(detallePedidoFarmacia.pedidoDeFarmacia.nroPedido, [])
            detallesRemito.append(detalle)
            #detallesRemito[detallePedidoFarmacia.pedidoDeFarmacia.nroPedido] = detallesRemito
    for pkPedido, detallesRemitoLaboratorio in remitosDeFarmacia.items():
        pedidoDeFarmacia = models.PedidoDeFarmacia.objects.get(pk=pkPedido)
        listaPedidosDeFarmacia.append(pedidoDeFarmacia)
        remitoFarmacia = models.RemitoDeFarmacia()
        remitoFarmacia.pedidoFarmacia = pedidoDeFarmacia
        remitoFarmacia.fecha = remitoLab.fecha
        remitoFarmacia.save()
        for detalle in detallesRemitoLaboratorio:
            #actualiza la cantidad pendiente del detalle pedido farmacia
            detallePedidoFarmacia = models.DetallePedidoDeFarmacia.objects.get(pk=detalle.detallePedidoLaboratorio.detallePedidoFarmacia.pk)
           
            detallePedidoFarmacia.cantidadPendiente -= detalle.cantidad
            detallePedidoFarmacia.save()

            detalleRemitoFarmacia = models.DetalleRemitoDeFarmacia()
            detalleRemitoFarmacia.cantidad = detalle.cantidad
            detalleRemitoFarmacia.lote = detalle.lote
            detalleRemitoFarmacia.detallePedidoDeFarmacia = detallePedidoFarmacia
            detalleRemitoFarmacia.remito = remitoFarmacia
            detalleRemitoFarmacia.save()

    #se actualiza el estado del pedido de farmacia
    for pedido in listaPedidosDeFarmacia:
        cantidadTotalDetalles = models.DetallePedidoDeFarmacia.objects.filter(pedidoDeFarmacia=pedido).count()
        cantidadDetallesCompletamenteSatisfechos = models.DetallePedidoDeFarmacia.objects.filter(pedidoDeFarmacia=pedido, cantidadPendiente=0).count()
        print "cantidadTotalDetalles", cantidadTotalDetalles, "\n"
        print "cantidadDetallesCompletamenteSatisfechos", cantidadDetallesCompletamenteSatisfechos, "\n"

        if cantidadTotalDetalles == cantidadDetallesCompletamenteSatisfechos:
            pedido.estado = "Enviado"
        else:
            pedido.estado = "Parcialmente Enviado"
        pedido.save()


def procesar_recepcion(sesion, pedido):
    remitoSesion = sesion['remitoRecepcion']['remito']
    detallesRemitoSesion = sesion['remitoRecepcion']['detalles']
    nuevosLotes = sesion['recepcionPedidoAlaboratorio']['nuevosLotes']
    actualizarLotes = sesion['recepcionPedidoAlaboratorio']['actualizarLotes']
    detalles = sesion['recepcionPedidoAlaboratorio']['detalles']

    crear_nuevos_lotes(nuevosLotes)
    actualizar_lotes(actualizarLotes)
    actualizar_pedido(pedido, detalles)

    remito = models.RemitoLaboratorio()
    remito.nroRemito = remitoSesion['nroRemito']
    remito.fecha = datetime.datetime.strptime(remitoSesion['fecha'], '%d/%m/%Y').date()
    remito.laboratorio = pedido.laboratorio
    remito.pedidoLaboratorio = pedido
    remito.save()
    for detalle in detallesRemitoSesion:       
        detalleRemito = models.DetalleRemitoLaboratorio()
        detalleRemito.remito = remito
        detalleRemito.cantidad = detalle['cantidad']
        detalleRemito.lote = mmodels.Lote.objects.get(numero= detalle['lote'])
        detalleRemito.detallePedidoLaboratorio = models.DetallePedidoAlaboratorio.objects.get(pk=detalle['detallePedidoLaboratorio'])
        detalleRemito.save()

    actualizar_pedidos_farmacia(remito)


#************************
# DEVOLUCION MEDICAMENTOS
#************************

def procesar_devolucion(laboratorio, lotes):
    remito = models.RemitoMedicamentosVencidos()
    remito.numero = get_next_nro_pedido_laboratorio(models.RemitoMedicamentosVencidos, "numero")
    remito.fecha = datetime.datetime.now()
    remito.laboratorio = laboratorio
    remito.save()

    for lote in lotes:
        detalleRemito = models.DetalleRemitoMedicamentosVencido()
        detalleRemito.remito = remito
        detalleRemito.medicamento = lote.medicamento
        detalleRemito.lote = lote
        detalleRemito.cantidad = lote.stock
        detalleRemito.save()
        lote.stock = 0
        lote.save()















def hay_medicamentos_con_stock():
    medicamentos = mmodels.Medicamento.objects.all()
    for medicamento in medicamentos:
        if medicamento.get_stock() > 0:
            return True     
    return False


