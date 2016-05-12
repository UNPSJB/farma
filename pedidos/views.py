#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.db.models import Q

from easy_pdf.views import PDFTemplateView
from jsonview.decorators import json_view
from crispy_forms.utils import render_crispy_form

import datetime
import re

from medicamentos import models as mmodels
from organizaciones import models as omodels
from pedidos import forms, models, utils


def get_filtros(get, modelo):
    mfilter = {}
    for filtro in modelo.FILTROS:
        if filtro in get and get[filtro]:
            attr = filtro
            value = get[filtro]
            if hasattr(modelo, "FILTERMAPPER") and filtro in modelo.FILTERMAPPER:
                attr = modelo.FILTERMAPPER[filtro]
            if value.isdigit():
                value = int(value)
            elif re.match(r"^[0-9]{2}/[0-9]{2}/[0-9]{4}$", value):
                fechaAux = value.split("/") # fecha separada por /
                fechaModificada = datetime.date(month=int(fechaAux[1]), day=int(fechaAux[0]), year=int(fechaAux[2]))
                value = fechaModificada
            mfilter[attr] = value
    return mfilter


def limpiar_sesion(list, session):
    for item in list:
        if item in session:
            del session[item]


# ******************************* PEDIDOS DE FARMACIA ******************************* #

@login_required(login_url='login')
def pedidosDeFarmacia(request):
    mfilters = get_filtros(request.GET, models.PedidoDeFarmacia)
    pedidos = models.PedidoDeFarmacia.objects.filter(**mfilters)
    estadisticas = {
        'total': models.PedidoDeFarmacia.objects.all().count(),
        'filtrados': pedidos.count()
    }
    return render(request, "pedidoDeFarmacia/pedidos.html", {"pedidos": pedidos, "filtros": request.GET, 'estadisticas': estadisticas})


@permission_required('usuarios.empleado_despacho_pedido', login_url='login')
@login_required(login_url='login')
def pedidoDeFarmacia_add(request):
    limpiar_sesion(["pedidoDeFarmacia", "detallesPedidoDeFarmacia"], request.session)
    if request.method == "POST":
        form = forms.PedidoDeFarmaciaForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            request.session['pedidoDeFarmacia'] = utils.crear_pedido_para_sesion(models.PedidoDeFarmacia, pedido)
            return redirect('detallesPedidoDeFarmacia')
    else:
           form = forms.PedidoDeFarmaciaForm()
    return render(request, "pedidoDeFarmacia/pedidoAdd.html", {"form": form})


@login_required(login_url='login')
def pedidoDeFarmacia_ver(request, id_pedido):
    pedido = models.PedidoDeFarmacia.objects.get(pk=id_pedido)
    detalles = models.DetallePedidoDeFarmacia.objects.filter(pedidoDeFarmacia=pedido)
    remitos = models.RemitoDeFarmacia.objects.filter(pedidoFarmacia__pk=id_pedido)
    return render(request, "pedidoDeFarmacia/pedidoVer.html",{"pedido": pedido, "detalles": detalles, "remitos": remitos})

@json_view
@login_required(login_url='login')
def pedidoDeFarmacia_verDetalles(request, id_pedido):
    detalles_json = []
    detalles = models.DetallePedidoDeFarmacia.objects.filter(pedidoDeFarmacia__pk=id_pedido)
    for detalle in detalles:
        detalles_json.append(detalle.to_json())
    return {'detalles': detalles_json}
    
@json_view
@login_required(login_url='login')
def pedidoDeFarmacia_verRemitos(request, id_pedido):
    remitos_json = []
    remitos = models.RemitoDeFarmacia.objects.filter(pedidoFarmacia__pk=id_pedido)
    for remito in remitos:
        json = remito.to_json()
        json['urlPdf'] = reverse('remitoDeFarmacia', args=[remito.pk])
        remitos_json.append(json)
    return {'remitos': remitos_json}

@json_view
@permission_required('usuarios.empleado_despacho_pedido', login_url='login')
@login_required(login_url='login')
def pedidoDeFarmacia_registrar(request):
    pedido = request.session['pedidoDeFarmacia']
    detalles = request.session['detallesPedidoDeFarmacia']
    mensaje_error = None
    if detalles:
        farmacia = omodels.Farmacia.objects.get(pk=pedido['farmacia']['id'])
        fecha = datetime.datetime.strptime(pedido['fecha'], '%d/%m/%Y').date()
        if not(models.PedidoDeFarmacia.objects.filter(pk=pedido["nroPedido"]).exists()):
            p = models.PedidoDeFarmacia(farmacia=farmacia, fecha=fecha)
            p.save()
            for detalle in detalles:
                medicamento = mmodels.Medicamento.objects.get(pk=detalle['medicamento']['id'])
                d = models.DetallePedidoDeFarmacia(pedidoDeFarmacia=p, medicamento=medicamento, cantidad=detalle['cantidad'])
                d.save()
            utils.procesar_pedido_de_farmacia(p)
            existeRemito = p.estado != "Pendiente"
            if existeRemito:
                nroRemito = models.RemitoDeFarmacia.objects.get(pedidoFarmacia__pk=p.pk)
                return {'success': True, 'existeRemito': True, 'nroRemito': nroRemito.id}
            else:
                return {'success': True, 'existeRemito': False}
        else:
            mensaje_error = "El pedido ya Existe!"
    else:
        mensaje_error = "No se puede registrar un pedido sin detalles"
    return {'success': False, 'mensaje-error': mensaje_error}


@permission_required('usuarios.empleado_despacho_pedido', login_url='login')
@login_required(login_url='login')
def detallesPedidoDeFarmacia(request):
    detalles = request.session.setdefault("detallesPedidoDeFarmacia", [])
    pedido = request.session['pedidoDeFarmacia']
    return render(request, "pedidoDeFarmacia/detallesPedido.html", {'pedido': pedido, 'detalles': detalles})


@json_view
@permission_required('usuarios.empleado_despacho_pedido', login_url='login')
@login_required(login_url='login')
def detallePedidoDeFarmacia_add(request):
    success = True
    form = forms.DetallePedidoDeFarmaciaForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            det = form.save(commit=False)
            detalles = request.session['detallesPedidoDeFarmacia']
            if not utils.existe_medicamento_en_pedido(detalles, det.medicamento.id):
                detalles.append(utils.crear_detalle_json(det, len(detalles) + 1))
                request.session['detallesPedidoDeFarmacia'] = detalles
                form = forms.DetallePedidoDeFarmaciaForm() #Nuevo form para seguir dando de alta
                form_html = render_crispy_form(form, context=RequestContext(request))
                return {'success': success, 'form_html': form_html, 'detalles': detalles}
            else:  # medicamento ya existe en el pedido
                return {'success': False}
        else:
            success = False
    form_html = render_crispy_form(form, context=RequestContext(request))
    return {'success': success, 'form_html': form_html}


@json_view
@permission_required('usuarios.empleado_despacho_pedido', login_url='login')
@login_required(login_url='login')
def detallePedidoDeFarmacia_update(request, id_detalle):
    detalles = request.session['detallesPedidoDeFarmacia']
    detalle = models.DetallePedidoDeFarmacia(cantidad=detalles[int(id_detalle) - 1]['cantidad'])
    if request.method == "POST":
        form = forms.UpdateDetallePedidoDeFarmaciaForm(request.POST, instance=detalle)
        if form.is_valid():
            det = form.save(commit=False)
            detalles[int(id_detalle) - 1]['cantidad'] = det.cantidad
            request.session['detallesPedidoDeFarmacia'] = detalles
            return {'success': True, 'detalles': detalles}
        else:
            form_html = render_crispy_form(form, context=RequestContext(request))
            return {'success': False, 'form_html': form_html}
    else:
        form = forms.UpdateDetallePedidoDeFarmaciaForm(instance=detalle)
    form_html = render_crispy_form(form, context=RequestContext(request))
    return {'form_html': form_html}


@json_view
@permission_required('usuarios.empleado_despacho_pedido', login_url='login')
@login_required(login_url='login')
def detallePedidoDeFarmacia_delete(request, id_detalle):
    detalles = request.session['detallesPedidoDeFarmacia']
    del detalles[int(id_detalle) - 1]
    for i in range(0, len(detalles)):
        detalles[i]['renglon'] = i + 1
    request.session['detallesPedidoDeFarmacia'] = detalles
    return {'detalles': detalles}


class remitoDeFarmacia(PDFTemplateView):
    template_name = "pedidoDeFarmacia/remitoDeFarmacia.html"

    def get_context_data(self, id_remito):
        remito = models.RemitoDeFarmacia.objects.get(id=id_remito)
        detallesRemito = models.DetalleRemitoDeFarmacia.objects.filter(remito=remito)
        return super(remitoDeFarmacia, self).get_context_data(
            pagesize="A4",
            remito=remito,
            detallesRemito=detallesRemito
        )


# ******************************* PEDIDOS DE CLINICA ******************************* #

@login_required(login_url='login')
def pedidosDeClinica(request):
    mfilters = get_filtros(request.GET, models.PedidoDeClinica)
    pedidos = models.PedidoDeClinica.objects.filter(**mfilters)
    estadisticas = {
        'total': models.PedidoDeClinica.objects.all().count(),
        'filtrados': pedidos.count()
    }
    return render(request, "pedidoDeClinica/pedidos.html", {"pedidos": pedidos, "filtros": request.GET, 'estadisticas': estadisticas})

@permission_required('usuarios.empleado_despacho_pedido', login_url='login')
@login_required(login_url='login')
def pedidoDeClinica_add(request):
    limpiar_sesion(["pedidoDeClinica", "detallesPedidoDeClinica"], request.session)
    if request.method == "POST":
        form = forms.PedidoDeClinicaForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido_json = pedido.to_json()
            pedido_json['nroPedido'] = utils.get_next_nro_pedido(models.PedidoDeClinica)
            request.session["pedidoDeClinica"] = pedido_json
            return redirect('detallesPedidoDeClinica')
    else:
           form = forms.PedidoDeClinicaForm()
    return render(request, "pedidoDeClinica/pedidoAdd.html", {"form": form})

@json_view
@permission_required('usuarios.empleado_despacho_pedido', login_url='login')
@login_required(login_url='login')
def get_obrasSociales(request, id_clinica):
    clinica = omodels.Clinica.objects.get(pk=id_clinica)
    obrasSociales = clinica.obraSocial.split(',')
    options = []
    for obraSocial in obrasSociales:
        options.append({'text':obraSocial, 'value':obraSocial})
    return options

@login_required(login_url='login')
def pedidoDeClinica_ver(request, id_pedido):
    pedido = models.PedidoDeClinica.objects.get(pk=id_pedido)
    detalles = models.DetallePedidoDeClinica.objects.filter(pedidoDeClinica=pedido)
    remitos = models.RemitoDeClinica.objects.filter(pedidoDeClinica__pk=id_pedido)
    return render(request, "pedidoDeClinica/pedidoVer.html", {"pedido": pedido, "detalles": detalles, "remitos":remitos})

@json_view
@login_required(login_url='login')
def pedidoDeClinica_verDetalles(request, id_pedido):
    detalles_json = []
    detalles = models.DetallePedidoDeClinica.objects.filter(pedidoDeClinica__pk=id_pedido)
    for detalle in detalles:
        detalles_json.append(detalle.to_json())
    return {'detalles': detalles_json}
    
@json_view
@login_required(login_url='login')
def pedidoDeClinica_verRemitos(request, id_pedido):
    remitos_json = []
    remitos = models.RemitoDeClinica.objects.filter(pedidoDeClinica__pk=id_pedido)
    for remito in remitos:
        json = remito.to_json()
        json['urlPdf'] = reverse('remitoDeClinica', args=[remito.pk])
        remitos_json.append(json)
    return {'remitos': remitos_json}

@json_view
@permission_required('usuarios.empleado_despacho_pedido', login_url='login')
@login_required(login_url='login')
def pedidoDeClinica_registrar(request):
    pedido = request.session["pedidoDeClinica"]
    detalles = request.session["detallesPedidoDeClinica"]
    mensaje_error = None
    if detalles:
        clinica = omodels.Clinica.objects.get(pk=pedido['clinica']['id'])
        fecha = datetime.datetime.strptime(pedido['fecha'], '%d/%m/%Y').date()
        obraSocial = pedido['obraSocial']
        medicoAuditor = pedido['medicoAuditor']
        if not(models.PedidoDeClinica.objects.filter(pk=pedido["nroPedido"]).exists()):
            p = models.PedidoDeClinica(clinica=clinica, fecha=fecha, obraSocial=obraSocial, medicoAuditor=medicoAuditor)
            p.save()
            for detalle in detalles:
                medicamento = mmodels.Medicamento.objects.get(pk=detalle['medicamento']['id'])
                d = models.DetallePedidoDeClinica(pedidoDeClinica=p, medicamento=medicamento, cantidad=detalle['cantidad'])
                d.save()
            utils.procesar_pedido_de_clinica(p)
            nroRemito = models.RemitoDeClinica.objects.get(pedidoDeClinica__pk=p.pk)
            return {'success': True, 'existeRemito': True, 'nroRemito': nroRemito.id}
        else:
            mensaje_error = "El pedido ya Existe!"
    else:
        mensaje_error = "No se puede registrar un pedido sin detalles"
    return {'success': False, 'mensaje-error': mensaje_error}

@permission_required('usuarios.empleado_despacho_pedido', login_url='login')
@login_required(login_url='login')
def detallesPedidoDeClinica(request):
    detalles = request.session.setdefault("detallesPedidoDeClinica", [])
    pedido = request.session["pedidoDeClinica"]
    medicamentos = utils.get_medicamentos_con_stock()
    medicamentos_stock = []
    for medicamento in medicamentos:
        medicamentos_stock.append({'id': medicamento.id, 'stock': medicamento.get_stock()})
    return render(request, "pedidoDeClinica/detallesPedido.html", {'pedido': pedido, 'detalles': detalles, 
                  'medicamentosStock': medicamentos_stock})


@json_view
@permission_required('usuarios.empleado_despacho_pedido', login_url='login')
@login_required(login_url='login')
def detallePedidoDeClinica_add(request):
    success = True
    form = forms.DetallePedidoDeClinicaForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            det = form.save(commit=False)
            detalles = request.session["detallesPedidoDeClinica"]
            if not utils.existe_medicamento_en_pedido(detalles, det.medicamento.id):
                detalles.append(utils.crear_detalle_json(det, len(detalles) + 1))
                request.session["detallesPedidoDeClinica"] = detalles
                form = forms.DetallePedidoDeClinicaForm() #Nuevo form para seguir dando de alta
                form_html = render_crispy_form(form, context=RequestContext(request))
                return {'success': success, 'form_html': form_html, 'detalles': detalles}
            else:  # medicamento ya existe en el pedido
                return {'success': False}
        else:
            success = False
    form_html = render_crispy_form(form, context=RequestContext(request))
    return {'success': success, 'form_html': form_html}


@json_view
@permission_required('usuarios.empleado_despacho_pedido', login_url='login')
@login_required(login_url='login')
def detallePedidoDeClinica_update(request, id_detalle):
    detalles = request.session['detallesPedidoDeClinica']
    detalle = models.DetallePedidoDeClinica(cantidad=detalles[int(id_detalle) - 1]['cantidad'])
    if request.method == "POST":
        form = forms.UpdateDetallePedidoDeClinicaForm(request.POST, instance=detalle)
        if form.is_valid(detalles[int(id_detalle) - 1]['medicamento']['id']):
            det = form.save(commit=False)
            detalles[int(id_detalle) - 1]['cantidad'] = det.cantidad
            request.session['detallesPedidoDeClinica'] = detalles
            return {'success': True, 'detalles': detalles}
        else:
            form_html = render_crispy_form(form, context=RequestContext(request))
            return {'success': False, 'form_html': form_html}
    else:
        form = forms.UpdateDetallePedidoDeClinicaForm(instance=detalle)
    form_html = render_crispy_form(form, context=RequestContext(request))
    return {'form_html': form_html}


@json_view
@permission_required('usuarios.empleado_despacho_pedido', login_url='login')
@login_required(login_url='login')
def detallePedidoDeClinica_delete(request, id_detalle):
    detalles = request.session['detallesPedidoDeClinica']
    del detalles[int(id_detalle) - 1]
    for i in range(0, len(detalles)):
        detalles[i]['renglon'] = i + 1
    request.session['detallesPedidoDeClinica'] = detalles
    return {'detalles': detalles}


class remitoDeClinica(PDFTemplateView):
    template_name = "pedidoDeClinica/remitoDeClinica.html"

    def get_context_data(self, id_remito):
        remito = models.RemitoDeClinica.objects.get(id=id_remito)
        detallesRemito = models.DetalleRemitoDeClinica.objects.filter(remito=remito)
        return super(remitoDeClinica, self).get_context_data(
            pagesize="A4",
            remito=remito,
            detallesRemito=detallesRemito
        )


# =================VISTAS DE PEDIDO A LABORATORIO NUEVAS=================#


@login_required(login_url='login')
def pedidosAlaboratorio(request):
    mfilters = get_filtros(request.GET, models.PedidoAlaboratorio)
    pedidos = models.PedidoAlaboratorio.objects.filter(**mfilters).exclude(estado="Cancelado")
    estadisticas = {
        'total': models.PedidoAlaboratorio.objects.all().exclude(estado="Cancelado").count(),
        'filtrados': pedidos.count()
    }
    return render(request, "pedidoAlaboratorio/pedidos.html", {"pedidos": pedidos, "filtros": request.GET, 'estadisticas': estadisticas})


@permission_required('usuarios.encargado_pedido', login_url='login')
@login_required(login_url='login')
def pedidoAlaboratorio_add(request):
    limpiar_sesion(['pedidoAlaboratorio', 'detallesPedidoAlaboratorio'], request.session)
    if request.method == 'POST': 
        form = forms.PedidoLaboratorioForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido_json = pedido.to_json()
            pedido_json['nroPedido'] = utils.get_next_nro_pedido(models.PedidoAlaboratorio)
            request.session['pedidoAlaboratorio'] = pedido_json
            request.session['detallesPedidoAlaboratorio'] = utils.get_detalles_a_pedir(pedido_json['laboratorio']['id'])
            return redirect('detallesPedidoAlaboratorio')
    else:
        form = forms.PedidoLaboratorioForm()
    return render(request, 'pedidoAlaboratorio/pedidoAdd.html', {'form': form})


@permission_required('usuarios.encargado_general', login_url='login')
@login_required(login_url='login')
def pedidoAlaboratorio_cancelar(request, id_pedido):
    pedido = models.PedidoAlaboratorio.objects.get(pk=id_pedido)
    utils.cancelar_pedido_a_laboratorio(pedido);
    return redirect('pedidosAlaboratorio')

@json_view
@login_required(login_url='login')
def pedidoAlaboratorio_verDetalles(request, id_pedido):
    detalles_json = []
    detalles = models.DetallePedidoAlaboratorio.objects.filter(pedido__pk=id_pedido)
    for detalle in detalles:
        detalles_json.append(detalle.to_json())
    return {'detalles': detalles_json}
    
@json_view
def pedidoAlaboratorio_verRemitos(request, id_pedido):
    remitos_json = []
    remitos = models.RemitoLaboratorio.objects.filter(pedidoLaboratorio__pk=id_pedido)
    for remito in remitos:
        json = remito.to_json()
        json['urlPdf'] = reverse('remitoDeLaboratorio', args=[remito.pk])
        remitos_json.append(json)
    return {'remitos': remitos_json}


@login_required(login_url='login')
def pedidoAlaboratorio_ver(request, id_pedido):
    pedido = models.PedidoAlaboratorio.objects.get(pk=id_pedido)
    detalles = models.DetallePedidoAlaboratorio.objects.filter(pedido=pedido)
    remitos = models.RemitoLaboratorio.objects.filter(pedidoLaboratorio__pk=id_pedido)
    return render(request, "pedidoAlaboratorio/pedidoVer.html", {'pedido': pedido, 'detalles': detalles, 'remitos': remitos})


@permission_required('usuarios.encargado_pedido', login_url='login')
@login_required(login_url='login')
def detallesPedidoAlaboratorio(request):
    pedido = request.session['pedidoAlaboratorio']
    detalles = request.session["detallesPedidoAlaboratorio"]
    return render(request, "pedidoAlaboratorio/detallesPedido.html", {'pedido': pedido, 'detalles': detalles})


@json_view
@permission_required('usuarios.encargado_pedido', login_url='login')
@login_required(login_url='login')
def detallePedidoAlaboratorio_add(request):
    success = True 
    id_laboratorio = request.session['pedidoAlaboratorio']['laboratorio']['id'] 
    if request.method == 'POST': 
        form = forms.DetallePedidoAlaboratorioFormFactory(id_laboratorio)(request.POST) 
        if form.is_valid(): 
            det = form.save(commit=False) 
            detalles = request.session["detallesPedidoAlaboratorio"] 
            if not utils.existe_medicamento_en_detalle_suelto(detalles, det.medicamento.id):
                detallePedidoAlaboratorio_json = utils.crear_detalle_json(det, len(detalles) + 1) 
                #detalle suelto no se corresponde con ningun detalle de pedido de farmacia
                detallePedidoAlaboratorio_json['detallePedidoFarmacia'] = -1 
                detalles.append(detallePedidoAlaboratorio_json) 
                request.session["detallesPedidoAlaboratorio"] = detalles 
                #Nuevo form para seguir dando de alta
                form = forms.DetallePedidoAlaboratorioFormFactory(id_laboratorio)() 
                form_html = render_crispy_form(form, context=RequestContext(request)) 
                return {'success': success, 'form_html': form_html, 'detalles': detalles}
            else:
                return {'success': False} 
        else: 
            success = False 
    else: 
        form = forms.DetallePedidoAlaboratorioFormFactory(id_laboratorio)() 
    form_html = render_crispy_form(form, context=RequestContext(request)) 
    return {'success': success, 'form_html': form_html} 



@json_view
@permission_required('usuarios.encargado_pedido', login_url='login')
@login_required(login_url='login')
def detallePedidoAlaboratorio_update(request, id_detalle):
    detalles = request.session['detallesPedidoAlaboratorio']
    detalle_session = detalles[int(id_detalle) - 1]
    if detalle_session['detallePedidoFarmacia'] == -1:
        detalle = models.DetallePedidoAlaboratorio(cantidad=detalle_session['cantidad'])
        if request.method == "POST":
            form = forms.UpdateDetallePedidoAlaboratorioForm(request.POST, instance=detalle)
            if form.is_valid():
                det = form.save(commit=False)
                detalles[int(id_detalle) - 1]['cantidad'] = det.cantidad
                request.session['detallesPedidoAlaboratorio'] = detalles
                return {'success': True, 'detalles': detalles}
            else:
                form_html = render_crispy_form(form, context=RequestContext(request))
                return {'success': False, 'form_html': form_html}
        else:
            form = forms.UpdateDetallePedidoAlaboratorioForm(instance=detalle)
        form_html = render_crispy_form(form, context=RequestContext(request))
        return {'form_html': form_html}


@json_view
@permission_required('usuarios.encargado_pedido', login_url='login')
@login_required(login_url='login')
def detallePedidoAlaboratorio_delete(request, id_detalle):
    detalles = request.session['detallesPedidoAlaboratorio']
    id = int(id_detalle)
    if id > 0 and id <= len(detalles):
        del detalles[int(id_detalle) - 1]
        for i in range(0, len(detalles)):
            detalles[i]['renglon'] = i + 1
        request.session['detallesPedidoAlaboratorio'] = detalles
    return {'detalles': detalles} 


@json_view
@permission_required('usuarios.encargado_pedido', login_url='login')
@login_required(login_url='login')
def pedidoAlaboratorio_registrar(request):
    pedido = request.session['pedidoAlaboratorio'] 
    detalles = request.session['detallesPedidoAlaboratorio'] 
    mensaje_error = None 
    if detalles: 
        laboratorio = omodels.Laboratorio.objects.get(pk=pedido['laboratorio']['id']) 
        fecha = datetime.datetime.strptime(pedido['fecha'], '%d/%m/%Y').date() 
        if not(models.PedidoAlaboratorio.objects.filter(pk=pedido["nroPedido"]).exists()): 
            p = models.PedidoAlaboratorio(laboratorio=laboratorio, fecha=fecha)
            p.save() 
            for detalle in detalles: 
                medicamento = mmodels.Medicamento.objects.get(pk=detalle['medicamento']['id']) 
                d = models.DetallePedidoAlaboratorio(pedido=p, medicamento=medicamento, cantidad=detalle['cantidad'], cantidadPendiente=detalle['cantidad']) 
                if detalle['detallePedidoFarmacia'] != -1: 
                    detallePedidoFarmacia = models.DetallePedidoDeFarmacia.objects.get(pk=detalle['detallePedidoFarmacia']) 
                    detallePedidoFarmacia.estaPedido = True 
                    detallePedidoFarmacia.save() 
                    d.detallePedidoFarmacia =  detallePedidoFarmacia 
                d.save() 
            return {'success': True} 
        else: 
            mensaje_error = "El pedido ya Existe!" 
    else: 
        mensaje_error = "No se puede registrar un pedido sin detalles" 
    return {'success': False, 'mensaje-error': mensaje_error} 


# ====================================== INICIO RECEPCION DE PEDIDO A LABORATORIO ======================================

@permission_required('usuarios.encargado_stock', login_url='login')
@login_required(login_url='login')
def recepcionPedidoAlaboratorio(request):
    mfilters = get_filtros(request.GET, models.PedidoAlaboratorio)
    pedidos = models.PedidoAlaboratorio.objects.filter(Q(estado='Pendiente')|Q(estado='Parcialmente Recibido'), **mfilters)
    estadisticas = {
        'total': models.PedidoAlaboratorio.objects.filter(Q(estado='Pendiente')|Q(estado='Parcialmente Recibido')).count(),
        'filtrados': pedidos.count()
    }
    return render(request, "recepcionPedidoALaboratorio/pedidos.html", {'pedidos': pedidos, "filtros": request.GET, 'estadisticas': estadisticas})


@permission_required('usuarios.encargado_stock', login_url='login')
@login_required(login_url='login')
def recepcionPedidoAlaboratorio_cargarPedido(request, id_pedido):
    limpiar_sesion(['recepcionPedidoAlaboratorio', 'remitoRecepcion'], request.session)
    utils.cargar_detalles(id_pedido, request.session)
    info = {'remito': {}, 'detalles': []}
    request.session['remitoRecepcion'] = info
    return redirect('recepcionPedidoAlaboratorio_registrarRecepcion', id_pedido)


@permission_required('usuarios.encargado_stock', login_url='login')
@login_required(login_url='login')
def recepcionPedidoAlaboratorio_controlPedido(request, id_pedido):
    pedido = models.PedidoAlaboratorio.objects.get(pk=id_pedido)
    detalles = request.session['recepcionPedidoAlaboratorio']['detalles']
    return render(request, "recepcionPedidoALaboratorio/controlPedido.html", {'pedido': pedido, 'detalles': detalles})


@permission_required('usuarios.encargado_stock', login_url='login')
@login_required(login_url='login')
def recepcionPedidoAlaboratorio_registrarRecepcion(request, id_pedido):
    if request.method == 'POST':
        form = forms.RegistrarRecepcionForm(request.POST)
        if form.is_valid():
            nroRemito = form.cleaned_data['nroRemito']
            fecha = form.cleaned_data['fechaRemito']
            fecha = fecha.strftime('%d/%m/%Y')
            info = {'remito': {'nroRemito':nroRemito, 'fecha': fecha}, 'detalles': []}
            request.session['remitoRecepcion'] = info

            return redirect('recepcionPedidoAlaboratorio_controlPedido', id_pedido)
    else:
        form = forms.RegistrarRecepcionForm()
        form.helper.form_action = reverse('recepcionPedidoAlaboratorio_registrarRecepcion', args=[id_pedido])

    return render(request, "recepcionPedidoALaboratorio/registrarRemito.html", {'form': form})


@permission_required('usuarios.encargado_stock', login_url='login')
@login_required(login_url='login')
def recepcionPedidoAlaboratorio_controlDetalle(request, id_pedido, id_detalle):
    if utils.hay_cantidad_pendiente(request.session['recepcionPedidoAlaboratorio']['detalles'], id_detalle):
        pedido = models.PedidoAlaboratorio.objects.get(pk=id_pedido)
        detalle = models.DetallePedidoAlaboratorio.objects.get(pk=id_detalle)
        lotesEnSesion = request.session['recepcionPedidoAlaboratorio']['nuevosLotes']
        if request.method == 'POST':
            form = forms.ControlDetallePedidoAlaboratorioFormFactory(detalle.medicamento.id, lotesEnSesion)(request.POST)
            posDetalle = utils.get_pos_detalle(request.session['recepcionPedidoAlaboratorio']['detalles'], detalle.renglon)
            infoDetalle = request.session['recepcionPedidoAlaboratorio']['detalles'][posDetalle]
            if form.is_valid(infoDetalle['cantidadPendiente']):
                utils.guardar_recepcion_detalle(request.session, detalle, form.clean())
                if '_volver' in request.POST:
                    return redirect('recepcionPedidoAlaboratorio_controlPedido', pedido.nroPedido)
                else:
                    return redirect('recepcionPedidoAlaboratorio_controlDetalle', pedido.nroPedido, detalle.renglon)
        else:
            if not utils.medicamento_tiene_lotes(detalle.medicamento, request.session['recepcionPedidoAlaboratorio']['nuevosLotes']):
                return redirect('recepcionPedidoAlaboratorio_controlDetalleConNuevoLote', pedido.nroPedido, detalle.renglon)
            form = forms.ControlDetallePedidoAlaboratorioFormFactory(detalle.medicamento.id, lotesEnSesion)()
            form.helper.form_action = reverse('recepcionPedidoAlaboratorio_controlDetalle', args=[pedido.nroPedido, detalle.renglon])
        return render(request, "recepcionPedidoALaboratorio/controlDetalle.html", {'btnNuevoLote': True, 'pedido': pedido, 'detalle': detalle, 'form': form})
    else:
        return redirect('recepcionPedidoAlaboratorio_controlPedido', id_pedido)


@permission_required('usuarios.encargado_stock', login_url='login')
@login_required(login_url='login')
def recepcionPedidoAlaboratorio_controlDetalleConNuevoLote(request, id_pedido, id_detalle):
    if utils.hay_cantidad_pendiente(request.session['recepcionPedidoAlaboratorio']['detalles'], id_detalle):
        pedido = models.PedidoAlaboratorio.objects.get(pk=id_pedido)
        detalle = models.DetallePedidoAlaboratorio.objects.get(pk=id_detalle)
        if request.method == 'POST':
            form = forms.ControlDetalleConNuevoLotePedidoAlaboratorioForm(request.POST)
            posDetalle = utils.get_pos_detalle(request.session['recepcionPedidoAlaboratorio']['detalles'], detalle.renglon)
            infoDetalle = request.session['recepcionPedidoAlaboratorio']['detalles'][posDetalle]
            if form.is_valid(infoDetalle['cantidadPendiente'], request.session['recepcionPedidoAlaboratorio']['nuevosLotes']):
                utils.guardar_recepcion_detalle_con_nuevo_lote(request.session, detalle, form.clean())
                if '_volver' in request.POST:
                    return redirect('recepcionPedidoAlaboratorio_controlPedido', pedido.nroPedido)
                else:
                    return redirect('recepcionPedidoAlaboratorio_controlDetalleConNuevoLote', pedido.nroPedido, detalle.renglon)
        else:       
            form = forms.ControlDetalleConNuevoLotePedidoAlaboratorioForm()
            form.helper.form_action = reverse('recepcionPedidoAlaboratorio_controlDetalleConNuevoLote', args=[pedido.nroPedido, detalle.renglon])
        existenLotes = False
        if utils.medicamento_tiene_lotes(detalle.medicamento, request.session['recepcionPedidoAlaboratorio']['nuevosLotes']):
            existenLotes = True
        return render(request, "recepcionPedidoALaboratorio/controlDetalle.html", {'btnNuevoLote': False, 'existenLotes': existenLotes, 'pedido': pedido, 'detalle': detalle, 'form': form})
    else:
        return redirect('recepcionPedidoAlaboratorio_controlPedido', id_pedido)


@permission_required('usuarios.encargado_stock', login_url='login')
@login_required(login_url='login')
def recepcionPedidoAlaboratorio_registrar(request, id_pedido):
    pedido = models.PedidoAlaboratorio.objects.get(pk=id_pedido)
    detalles = request.session['recepcionPedidoAlaboratorio']['detalles']
    nuevosLotes = request.session['recepcionPedidoAlaboratorio']['nuevosLotes']
    actualizarLotes = request.session['recepcionPedidoAlaboratorio']['actualizarLotes']

    if len(nuevosLotes) > 0 or len(actualizarLotes) > 0:
        utils.procesar_recepcion(request.session, pedido)
        return render(request, "recepcionPedidoALaboratorio/controlPedido.html", {'pedido': pedido, 'detalles': detalles, 'modalSuccess': True})

    return render(request, "recepcionPedidoALaboratorio/controlPedido.html", {'pedido': pedido, 'detalles': detalles, 'modalError': True})


class remitoDeLaboratorio(PDFTemplateView):
    template_name = "pedidoAlaboratorio/remitoDeLaboratorio.html"

    def get_context_data(self, id_remito):
        remito = models.RemitoLaboratorio.objects.get(nroRemito=id_remito)
        detallesRemito = models.DetalleRemitoLaboratorio.objects.filter(remito=remito)
        return super(remitoDeLaboratorio, self).get_context_data(
            pagesize="A4",
            remito=remito,
            detallesRemito=detallesRemito
        )


@permission_required('usuarios.encargado_medicamentos_vencidos', login_url='login')
@login_required(login_url='login')
def devolucionMedicamentosVencidos(request):
    if request.method == 'POST':
        form = forms.DevolucionMedicamentosForm(request.POST)
        if form.is_valid():
            formLaboratorio = form.cleaned_data.get('laboratorio')
            return redirect('devolucionMedicamentosVencidos_detalle', formLaboratorio.id)
    else:
        form = forms.DevolucionMedicamentosForm()
    return render(request, 'devolucionMedicamentosVencidos/devolucionMedicamentosVencidos.html', {'form': form})

@permission_required('usuarios.encargado_medicamentos_vencidos', login_url='login')
@login_required(login_url='login')
def devolucionMedicamentosVencidos_detalle(request, id_laboratorio):
    laboratorio = omodels.Laboratorio.objects.get(pk=id_laboratorio)
    medicamentos = mmodels.Medicamento.objects.filter(laboratorio=laboratorio) # todos los medicamentos
    lista = []

    for m in medicamentos:
        lista.append(m.pk)

    lt = datetime.date.today() + datetime.timedelta(weeks=26)  # fecha vencimiento.(limite)
    lotes = mmodels.Lote.objects.filter(fechaVencimiento__lte=lt, medicamento__pk__in=lista, stock__gt=0)

    return render(request, "devolucionMedicamentosVencidos/devolucionMedicamentosVencidos_detalle.html",
                  {'lotes': lotes, 'laboratorioId': id_laboratorio, 'fecha': datetime.datetime.now(),
                  'numero': utils.get_next_nro_pedido_laboratorio(models.RemitoMedicamentosVencidos, "numero")})


@permission_required('usuarios.encargado_medicamentos_vencidos', login_url='login')
@login_required(login_url='login')
def devolucionMedicamentosVencidos_registrar(request, id_laboratorio):
    laboratorio = omodels.Laboratorio.objects.get(pk=id_laboratorio)
    medicamentos = mmodels.Medicamento.objects.filter(laboratorio=laboratorio)  # todos los medicamentos
    lista = []

    for m in medicamentos:
        lista.append(m.pk)

    lt = datetime.date.today() + datetime.timedelta(weeks=26)  # fecha vencimiento.(limite)
    lotes = mmodels.Lote.objects.filter(fechaVencimiento__lte=lt, medicamento__pk__in=lista, stock__gt=0)

    utils.procesar_devolucion(laboratorio, lotes)
    return render(request, "devolucionMedicamentosVencidos/devolucionMedicamentosVencidos_detalle.html",
                  {'laboratorioId': id_laboratorio, 'abrirModal': True, 'fecha': datetime.datetime.now(),
                  'numero': utils.get_next_nro_pedido_laboratorio(models.RemitoMedicamentosVencidos, "numero")-1})


class remitoDevolucion(PDFTemplateView):
    template_name = "devolucionMedicamentosVencidos/remitoDevolucion.html"

    def get_context_data(self, id_remito):
        remito = models.RemitoMedicamentosVencidos.objects.get(numero=id_remito)
        detallesRemito = models.DetalleRemitoMedicamentosVencido.objects.filter(remito=remito)
        return super(remitoDevolucion, self).get_context_data(
            pagesize="A4",
            remito=remito,
            detallesRemito=detallesRemito
        )