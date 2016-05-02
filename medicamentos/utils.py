#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .import models
from pedidos import models as pmodels
from django.db.models import Q

def puedo_eliminar_medicamento(id_medicamento):
	infoBaja = {'success': True, 'informe': ''}
	contadorPendientesAlaboratorio = 0
	contadorPendientesDeFarmacia = 0
	contadorLotesActivos = 0
	medicamento = models.Medicamento.objects.get(pk=id_medicamento)
	mensajeInforme = ''

	print medicamento.get_lotes_activos()
	# Medicamento pendiente en pedidos a laboratorio ?
	pendienteEnPedidosAlaboratorio = pmodels.PedidoAlaboratorio.objects.filter(Q(estado='Pendiente')|Q(estado='Parcialmente Recibido'))
	for pedido in pendienteEnPedidosAlaboratorio:
		contador = pmodels.DetallePedidoAlaboratorio.objects.filter(pedido=pedido, medicamento__pk=id_medicamento, cantidadPendiente__gt = 0).count()
		if contador > 0:
			contadorPendientesAlaboratorio += 1

	pendienteEnPedidosDeFarmacia = pmodels.PedidoDeFarmacia.objects.filter(Q(estado='Pendiente')|Q(estado='Parcialmente Enviado'))
	for pedido in pendienteEnPedidosDeFarmacia:
		contador = pmodels.DetallePedidoDeFarmacia.objects.filter(pedidoDeFarmacia=pedido, medicamento__pk=id_medicamento, cantidadPendiente__gt = 0).count()
		print "***************", contador,"****************"
		if contador > 0:
			contadorPendientesDeFarmacia += 1

	contadorLotesActivos = medicamento.get_lotes_activos().count()

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