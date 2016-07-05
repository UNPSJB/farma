#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db.models import Q
from . import models
from pedidos import models as pmodels
from medicamentos import models as mmodels
from collections import OrderedDict
from django.db.models import Sum
from pedidos.views import get_filtros
import itertools
import datetime
import re


def puedo_eliminar_farmacia(id_farmacia):
    infoBaja = {'success': True, 'informe': ''}
    farmacia = models.Farmacia.objects.get(pk=id_farmacia)
    contadorPedidosDeFarmacia = 0
    mensajeInforme = ''
    contadorPedidosDeFarmacia = pmodels.PedidoDeFarmacia.objects.filter(farmacia=farmacia).filter(Q(estado='Pendiente') | Q(estado='Parcialmente Enviado')).count()
    if contadorPedidosDeFarmacia > 0:
        mensajeInforme += "Hay " + str(contadorPedidosDeFarmacia)
        if contadorPedidosDeFarmacia == 1:
            mensajeInforme += " Pedido De Farmacia vinculados a la misma que aún no ha sido completamente enviado"
        else:
            mensajeInforme += " Pedidos De Farmacia vinculados a la misma que aún no han sido completamente enviados"

    infoBaja['success'] = contadorPedidosDeFarmacia == 0
    infoBaja['informe'] = mensajeInforme
    return infoBaja


def puedo_eliminar_laboratorio(id_laboratorio):
    infoBaja = {'success': True, 'informe': ''}
    laboratorio = models.Laboratorio.objects.get(pk=id_laboratorio)
    contadorPedidosPendientesAlaboratorio = 0
    contadorMedicamentosConStock = 0
    mensajeInforme = ''

    contadorPedidosPendientesAlaboratorio = pmodels.PedidoAlaboratorio.objects.filter(laboratorio=laboratorio).filter(Q(estado='Pendiente') | Q(estado='Parcialmente Recibido')).count()

    medicamentosDelLaboratorio = mmodels.Medicamento.objects.filter(laboratorio=laboratorio)
    for medicamento in medicamentosDelLaboratorio:
        if medicamento.get_stock() > 0:
            contadorMedicamentosConStock += 1

    if contadorPedidosPendientesAlaboratorio > 0:
        mensajeInforme += "Hay " + str(contadorPedidosPendientesAlaboratorio)
        if contadorPedidosPendientesAlaboratorio == 1:
            mensajeInforme += " Pedido A Laboratorio vinculado al mismo que aún no ha sido completamente recepcionado;"
        else:
            mensajeInforme += " Pedidos A Laboratorio vinculados al mismo que aún no han sido completamente recepcionados;"

    if contadorMedicamentosConStock > 0:
        mensajeInforme += "Hay " + str(contadorMedicamentosConStock)
        if contadorMedicamentosConStock == 1:
            mensajeInforme += " Medicamento con stock vinculado a este laboratorio;"
        else:
            mensajeInforme += " Medicamentos con stock vinculados a este laboratorio;"

    infoBaja['success'] = contadorPedidosPendientesAlaboratorio == 0 and contadorMedicamentosConStock == 0
    infoBaja['informe'] = mensajeInforme
    return infoBaja



