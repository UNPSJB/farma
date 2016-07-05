#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .import models
from pedidos import models as pmodels
from django.db.models import Q
from collections import OrderedDict
from pedidos.views import get_filtros
import itertools


def puedo_eliminar_medicamento(id_medicamento):
    infoBaja = {'success': True, 'informe': ''}
    contadorPendientesAlaboratorio = 0
    contadorPendientesDeFarmacia = 0
    contadorLotesActivos = 0
    medicamento = models.Medicamento.objects.get(pk=id_medicamento)
    mensajeInforme = ''

    pendienteEnPedidosAlaboratorio = pmodels.PedidoAlaboratorio.objects.filter(Q(estado='Pendiente') | Q(estado='Parcialmente Recibido'))
    for pedido in pendienteEnPedidosAlaboratorio:
        contador = pmodels.DetallePedidoAlaboratorio.objects.filter(pedido=pedido, medicamento__pk=id_medicamento, cantidadPendiente__gt=0).count()
        if contador > 0:
            contadorPendientesAlaboratorio += 1

    pendienteEnPedidosDeFarmacia = pmodels.PedidoDeFarmacia.objects.filter(Q(estado='Pendiente') | Q(estado='Parcialmente Enviado'))
    for pedido in pendienteEnPedidosDeFarmacia:
        contador = pmodels.DetallePedidoDeFarmacia.objects.filter(pedidoDeFarmacia=pedido, medicamento__pk=id_medicamento, cantidadPendiente__gt=0).count()
        if contador > 0:
            contadorPendientesDeFarmacia += 1

    contadorLotesActivos = medicamento.get_lotes_con_stock().count()

    if contadorPendientesAlaboratorio > 0:
        mensajeInforme += "Hay " + str(contadorPendientesAlaboratorio)
        if contadorPendientesAlaboratorio == 1:
            mensajeInforme += " Pedido A Laboratorio que contiene"
        else:
            mensajeInforme += " Pedidos A Laboratorio que contienen"
        mensajeInforme += " al menos un detalle pendiente vinculado a este medicamento;"

    if contadorPendientesDeFarmacia > 0:
        mensajeInforme += "Hay " + str(contadorPendientesDeFarmacia)
        if contadorPendientesDeFarmacia == 1:
            mensajeInforme += " Pedido De Farmacia que contiene"
        else:
            mensajeInforme += " Pedidos De Farmacia que contienen"
        mensajeInforme += " un detalle pendiente vinculado a este medicamento;"

    if contadorLotesActivos > 0:
        mensajeInforme += "Hay " + str(contadorLotesActivos)
        if contadorLotesActivos == 1:
            mensajeInforme += " lote activo vinculado"
        else:
            mensajeInforme += " lotes activos vinculados"
        mensajeInforme += " a este medicamento"

    infoBaja['success'] = contadorPendientesAlaboratorio == 0 and contadorPendientesDeFarmacia == 0 and contadorLotesActivos == 0
    infoBaja['informe'] = mensajeInforme
    return infoBaja


def puedo_eliminar_monodroga(id_monodroga):
    infoBaja = {'success': True, 'informe': ''}
    mensajeInforme = ''
    contadorMedicamentosConMonodroga = models.Dosis.objects.filter(monodroga__pk=id_monodroga).count()

    if contadorMedicamentosConMonodroga > 0:
        mensajeInforme += "Hay " + str(contadorMedicamentosConMonodroga)
        if contadorMedicamentosConMonodroga == 1:
            mensajeInforme += " Medicamento que contiene esta monodroga;"
        else:
            mensajeInforme += " Medicamentos que contienen esta monodroga;"

    infoBaja['success'] = contadorMedicamentosConMonodroga == 0
    infoBaja['informe']  = mensajeInforme
    return infoBaja


def puedo_eliminar_nombreFantasia(id_nombreFantasia):
    infoBaja = {'success': True, 'informe': ''}
    mensajeInforme = ''
    contadorMedicamentosConNombreFantasia = models.Medicamento.objects.filter(nombreFantasia__pk=id_nombreFantasia).count()

    if contadorMedicamentosConNombreFantasia > 0:
        mensajeInforme += "Hay " + str(contadorMedicamentosConNombreFantasia)
        if contadorMedicamentosConNombreFantasia == 1:
            mensajeInforme += " Medicamento que contiene este nombre fantasía;"
        else:
            mensajeInforme += " Medicamentos que contienen este nombre fantasía;"

    infoBaja['success'] = contadorMedicamentosConNombreFantasia == 0
    infoBaja['informe']  = mensajeInforme
    return infoBaja


def puedo_eliminar_presentacion(id_presentacion):
    infoBaja = {'success': True, 'informe': ''}
    mensajeInforme = ''
    contadorMedicamentosConPresentacion = models.Medicamento.objects.filter(presentacion__pk=id_presentacion).count()

    if contadorMedicamentosConPresentacion > 0:
        mensajeInforme += "Hay " + str(contadorMedicamentosConPresentacion)
        if contadorMedicamentosConPresentacion == 1:
            mensajeInforme += " Medicamento que contiene esta presentación;"
        else:
            mensajeInforme += " Medicamentos que contienen esta presentación;"

    infoBaja['success'] = contadorMedicamentosConPresentacion == 0
    infoBaja['informe']  = mensajeInforme
    return infoBaja


def top_10_cantidad_medicamentos(get):
    mfiltersPedidoDeFarmacia = get_filtros(get, pmodels.PedidoDeFarmacia)
    mfiltersPedidoDeClinica = get_filtros(get, pmodels.PedidoDeClinica)
    pedidosDeFarmacia = pmodels.PedidoDeFarmacia.objects.filter(**mfiltersPedidoDeFarmacia)
    pedidosDeClinica = pmodels.PedidoDeClinica.objects.filter(**mfiltersPedidoDeClinica)
    estadisticas = {}

    cantidadTotalMedicamentoEnPedidos = 0

    for pedido in pedidosDeFarmacia:
        for detalle in pedido.get_detalles():
            cantidadMedicamento = detalle.cantidad
            medicamento = detalle.medicamento.__str__()
            if medicamento in estadisticas:
                estadisticas[medicamento] += cantidadMedicamento
            else:
                estadisticas[medicamento] = cantidadMedicamento
            cantidadTotalMedicamentoEnPedidos += cantidadMedicamento

    for pedido in pedidosDeClinica:
        for detalle in pedido.get_detalles():
            cantidadMedicamento = detalle.cantidad
            medicamento = detalle.medicamento.__str__()
            if medicamento in estadisticas:
                estadisticas[medicamento] += cantidadMedicamento
            else:
                estadisticas[medicamento] = cantidadMedicamento
            cantidadTotalMedicamentoEnPedidos += cantidadMedicamento

    # ordeno y selecciono top10
    top = OrderedDict(sorted(estadisticas.items(), key=lambda t: t[1], reverse=True))
    top10 = dict(itertools.islice(top.items(), 10))
    top10 = OrderedDict(sorted(top10.items(), key=lambda t: t[1], reverse=True))

    estadisticas = {
        'columnChart': {'medicamentos': [], 'cantidades': []},
        'pieChart': [],
        'excel': []
    }

    resto = cantidadTotalMedicamentoEnPedidos
    for medicamento, cantidad in top10.items():
        estadisticas['columnChart']['medicamentos'].append(medicamento)
        estadisticas['columnChart']['cantidades'].append(cantidad)

        avg = float("%.2f" % ((cantidad * 100) / float(cantidadTotalMedicamentoEnPedidos)))
        estadisticas['pieChart'].append({'name': medicamento, 'y': avg})

        estadisticas['excel'].append({'medicamento': medicamento, 'cantidad': cantidad})

        resto -= cantidad

    if resto > 0:
        avg = float("%.2f" % ((resto * 100) / float(cantidadTotalMedicamentoEnPedidos)))
        estadisticas['pieChart'].append({'name': u'Otros', 'y': avg})

    return estadisticas


def top_10_pedido_medicamentos(get):
    mfiltersPedidoDeFarmacia = get_filtros(get, pmodels.PedidoDeFarmacia)
    mfiltersPedidoDeClinica = get_filtros(get, pmodels.PedidoDeClinica)
    pedidosDeFarmacia = pmodels.PedidoDeFarmacia.objects.filter(**mfiltersPedidoDeFarmacia)
    pedidosDeClinica = pmodels.PedidoDeClinica.objects.filter(**mfiltersPedidoDeClinica)
    estadisticas = {}

    totalPedidosDeMedicamentos = 0

    for pedido in pedidosDeFarmacia:
        for detalle in pedido.get_detalles():
            medicamento = detalle.medicamento.__str__()
            if medicamento in estadisticas:
                estadisticas[medicamento] += 1
            else:
                estadisticas[medicamento] = 1
        totalPedidosDeMedicamentos += 1

    for pedido in pedidosDeClinica:
        for detalle in pedido.get_detalles():
            medicamento = detalle.medicamento.__str__()
            if medicamento in estadisticas:
                estadisticas[medicamento] += 1
            else:
                estadisticas[medicamento] = 1
        totalPedidosDeMedicamentos += 1

    # ordeno y selecciono top10
    top = OrderedDict(sorted(estadisticas.items(), key=lambda t: t[1], reverse=True))
    top10 = dict(itertools.islice(top.items(), 10))
    top10 = OrderedDict(sorted(top10.items(), key=lambda t: t[1], reverse=True))

    estadisticas = {
        'columnChart': {'medicamentos': [], 'cantidades': []},
        'pieChart': [],
        'excel': []
    }

    resto = totalPedidosDeMedicamentos
    for medicamento, cantidad in top10.items():
        estadisticas['columnChart']['medicamentos'].append(medicamento)
        estadisticas['columnChart']['cantidades'].append(cantidad)

        avg = float("%.2f" % ((cantidad * 100) / float(totalPedidosDeMedicamentos)))
        estadisticas['pieChart'].append({'name': medicamento, 'y': avg})

        estadisticas['excel'].append({'medicamento': medicamento, 'cantidad': cantidad})

        resto -= cantidad

    if resto > 0:
        avg = float("%.2f" % ((resto * 100) / float(totalPedidosDeMedicamentos)))
        estadisticas['pieChart'].append({'name': u'Otros', 'y': avg})

    return estadisticas


def top_10_organizaciones_cantidad_medicamentos(get_filtros, valores):
    filtros = {'desde': valores['desde'], 'hasta': valores['hasta']}
    mfiltersPedidoDeFarmacia = get_filtros(filtros, pmodels.PedidoDeFarmacia)
    mfiltersPedidoDeClinica = get_filtros(filtros, pmodels.PedidoDeClinica)
    pedidosDeFarmacia = pmodels.PedidoDeFarmacia.objects.filter(**mfiltersPedidoDeFarmacia)
    pedidosDeClinica = pmodels.PedidoDeClinica.objects.filter(**mfiltersPedidoDeClinica)
    med = valores['medicamento']
    estadisticas = {}

    totalVentasMedicamento = 0

    for pedido in pedidosDeFarmacia:
        farmacia = "Farmacia "+pedido.farmacia.razonSocial
        for detalle in pedido.get_detalles():
            if detalle.medicamento == med:
                if farmacia in estadisticas:
                    estadisticas[farmacia] += detalle.cantidad
                else:
                    estadisticas[farmacia] = detalle.cantidad
                totalVentasMedicamento += detalle.cantidad
                break

    for pedido in pedidosDeClinica:
        clinica = "Clinica " + pedido.clinica.razonSocial
        for detalle in pedido.get_detalles():
            if detalle.medicamento == med:
                if clinica in estadisticas:
                    estadisticas[clinica] += detalle.cantidad
                else:
                    estadisticas[clinica] = detalle.cantidad
                totalVentasMedicamento += detalle.cantidad
                break

    # ordeno y selecciono top10
    top = OrderedDict(sorted(estadisticas.items(), key=lambda t: t[1], reverse=True))
    top10 = dict(itertools.islice(top.items(), 10))
    top10 = OrderedDict(sorted(top10.items(), key=lambda t: t[1], reverse=True))

    estadisticas = {
        'columnChart': {'organizaciones': [], 'cantidades': []},
        'pieChart': [],
        'excel': {'medicamento': '', 'datos': []}
    }

    resto = totalVentasMedicamento
    for organizacion, cantidad in top10.items():
        estadisticas['columnChart']['organizaciones'].append(organizacion)
        estadisticas['columnChart']['cantidades'].append(cantidad)

        avg = float("%.2f" % ((cantidad * 100) / float(totalVentasMedicamento)))
        estadisticas['pieChart'].append({'name': organizacion, 'y': avg})

        estadisticas['excel']['datos'].append({'organizacion': organizacion, 'cantidad': cantidad})

        resto -= cantidad

    estadisticas['excel']['medicamento'] = med.__str__()

    if resto > 0:
        avg = float("%.2f" % ((resto * 100) / float(totalVentasMedicamento)))
        estadisticas['pieChart'].append({'name': u'Otros', 'y': avg})

    return estadisticas


def top_10_organizaciones_pedidos_medicamentos(get_filtros, valores):
    filtros = {'desde': valores['desde'], 'hasta': valores['hasta']}
    mfiltersPedidoDeFarmacia = get_filtros(filtros, pmodels.PedidoDeFarmacia)
    mfiltersPedidoDeClinica = get_filtros(filtros, pmodels.PedidoDeClinica)
    pedidosDeFarmacia = pmodels.PedidoDeFarmacia.objects.filter(**mfiltersPedidoDeFarmacia)
    pedidosDeClinica = pmodels.PedidoDeClinica.objects.filter(**mfiltersPedidoDeClinica)
    med = valores['medicamento']
    estadisticas = {}

    totalSolicitudesMedicamento = 0

    for pedido in pedidosDeFarmacia:
        farmacia = "Farmacia "+pedido.farmacia.razonSocial
        for detalle in pedido.get_detalles():
            if detalle.medicamento == med:
                if farmacia in estadisticas:
                    estadisticas[farmacia] += 1
                else:
                    estadisticas[farmacia] = 1
                totalSolicitudesMedicamento += 1
                break

    for pedido in pedidosDeClinica:
        clinica = "Clinica " + pedido.clinica.razonSocial
        for detalle in pedido.get_detalles():
            if detalle.medicamento == med:
                if clinica in estadisticas:
                    estadisticas[clinica] += 1
                else:
                    estadisticas[clinica] = 1
                totalSolicitudesMedicamento += 1
                break

    # ordeno y selecciono top10
    top = OrderedDict(sorted(estadisticas.items(), key=lambda t: t[1], reverse=True))
    top10 = dict(itertools.islice(top.items(), 10))
    top10 = OrderedDict(sorted(top10.items(), key=lambda t: t[1], reverse=True))

    estadisticas = {
        'columnChart': {'organizaciones': [], 'cantidades': []},
        'pieChart': [],
        'excel': {'medicamento': '', 'datos': []}
    }

    resto = totalSolicitudesMedicamento
    for organizacion, cantidad in top10.items():
        estadisticas['columnChart']['organizaciones'].append(organizacion)
        estadisticas['columnChart']['cantidades'].append(cantidad)

        avg = float("%.2f" % ((cantidad * 100) / float(totalSolicitudesMedicamento)))
        estadisticas['pieChart'].append({'name': organizacion, 'y': avg})

        estadisticas['excel']['datos'].append({'organizacion': organizacion, 'cantidad': cantidad})

        resto -= cantidad

    estadisticas['excel']['medicamento'] = med.__str__()

    if resto > 0:
        avg = float("%.2f" % ((resto * 100) / float(totalSolicitudesMedicamento)))
        estadisticas['pieChart'].append({'name': u'Otros', 'y': avg})

    return estadisticas
