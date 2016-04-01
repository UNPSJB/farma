#!/usr/bin/python
# -*- encoding: utf-8 -*-
from easy_pdf.views import PDFTemplateView
from django.db.models import Q # Herramienta que nos permite "darle de comer" expresiones con OR a los filter

from medicamentos import models as mmodels
from organizaciones import models as omodels

# Create your views here.
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404, RequestContext
from jsonview.decorators import json_view
from pedidos import forms, models, utils
from organizaciones.models import Farmacia, Clinica, Laboratorio
from django.contrib.auth.decorators import login_required
from crispy_forms.utils import render_crispy_form
from django.contrib.auth import decorators as authd
from medicamentos.models import Medicamento, Lote
import datetime
import re

# Create your views here.

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
                fechaModificada =datetime.date(month=int(fechaAux[0]),day=int(fechaAux[1]), year=int(fechaAux[2]))
                value = fechaModificada
            mfilter[attr] = value

    return mfilter

def limpiar_sesion(pedido, detalles, session):
    if pedido in session:
        del session[pedido]
    if detalles in session:
        del session[detalles]

def get_next_nro_pedido(m, nombrePk):
    nro = None
    try:
        nro = m.objects.latest(nombrePk).nroPedido + 1
    except m.DoesNotExist:
        nro = 1
    return nro

def get_next_nro_pedido_laboratorio(m, nombrePk): #FUNCION TEMPORAL!!!
    nro = None
    try:
        nro = m.objects.latest(nombrePk).numero + 1
    except m.DoesNotExist:
        nro = 1
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

# ******************************* PEDIDOS DE FARMACIA ******************************* #

@login_required(login_url='login')
def pedidosDeFarmacia(request):
    mfilters = get_filtros(request.GET, models.PedidoDeFarmacia)
    pedidos = models.PedidoDeFarmacia.objects.filter(**mfilters)
    return render(request, "pedidoDeFarmacia/pedidos.html", {"pedidos": pedidos, "filtros": request.GET})

@login_required(login_url='login')
def pedidoDeFarmacia_add(request):
    limpiar_sesion("pedidoDeFarmacia", "detallesPedidoDeFarmacia", request.session)
    if request.method == "POST":
        form = forms.PedidoDeFarmaciaForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido_json = pedido.to_json()
            pedido_json['nroPedido'] = get_next_nro_pedido(models.PedidoDeFarmacia, "nroPedido")
            request.session['pedidoDeFarmacia'] = pedido_json
            return redirect('detallesPedidoDeFarmacia')
    else:
           form = forms.PedidoDeFarmaciaForm()
    return render(request, "pedidoDeFarmacia/pedidoAdd.html", {"form": form})


@login_required(login_url='login')
def pedidoDeFarmacia_ver(request, id_pedido):
    pedido = get_object_or_404(models.PedidoDeFarmacia,pk=id_pedido)
    detalles = models.DetallePedidoDeFarmacia.objects.filter(pedidoDeFarmacia=pedido)
    remitos = models.RemitoDeFarmacia.objects.filter(pedidoFarmacia__pk=id_pedido)
    return render(request, "pedidoDeFarmacia/pedidoVer.html",{"pedido": pedido, "detalles": detalles, "remitos": remitos})


@json_view
@login_required(login_url='login')
@authd.permission_required(perm="add_pedidodefarmacia")
@authd.permission_required(perm="change_pedidodefarmacia")
def pedidoDeFarmacia_registrar(request):
    pedido = request.session['pedidoDeFarmacia']
    detalles = request.session['detallesPedidoDeFarmacia']
    mensaje_error = None
    if detalles:
        farmacia = get_object_or_404(Farmacia, pk=pedido['farmacia']['id'])
        fecha = datetime.datetime.strptime(pedido['fecha'], '%d/%m/%Y').date()
        if not(models.PedidoDeFarmacia.objects.filter(pk=pedido["nroPedido"]).exists()):
            p = models.PedidoDeFarmacia(farmacia=farmacia, fecha=fecha)
            p.save()
            for detalle in detalles:
                medicamento = get_object_or_404(Medicamento, pk=detalle['medicamento']['id'])
                d = models.DetallePedidoDeFarmacia(pedidoDeFarmacia=p, medicamento=medicamento, cantidad=detalle['cantidad'])
                d.save()
            utils.procesar_pedido(p)
            existeRemito = p.estado != "Pendiente"
            return {'success': True, 'existeRemito': existeRemito}
        else:
            mensaje_error = "El pedido ya Existe!"
    else:
        mensaje_error = "No se puede registrar un pedido sin detalles"
    return {'success': False, 'mensaje-error': mensaje_error}


@login_required(login_url='login')
def detallesPedidoDeFarmacia(request):
    #del request.session['detalles']
    detalles = request.session.setdefault("detallesPedidoDeFarmacia", [])
    pedido = request.session['pedidoDeFarmacia']
    return render(request, "pedidoDeFarmacia/detallesPedido.html", {'pedido': pedido, 'detalles': detalles})


@json_view
@login_required(login_url='login')
def detallePedidoDeFarmacia_add(request):
    success = True
    form = forms.DetallePedidoDeFarmaciaForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            det = form.save(commit=False)
            detalles = request.session['detallesPedidoDeFarmacia']
            if not existe_medicamento_en_pedido(detalles, det.medicamento.id):
                detalles.append(crear_detalle_json(det, len(detalles) + 1))
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
@login_required(login_url='login')
def detallePedidoDeFarmacia_delete(request, id_detalle):
    detalles = request.session['detallesPedidoDeFarmacia']
    del detalles[int(id_detalle) - 1]
    for i in range(0, len(detalles)):
        detalles[i]['renglon'] = i + 1
    request.session['detallesPedidoDeFarmacia'] = detalles
    return {'detalles': detalles}

class remitoFarmacia(PDFTemplateView):
    template_name = "pedidoDeFarmacia/remitoFarmacia.html"

    def get_context_data(self, id_pedido):
        remito = models.RemitoDeFarmacia.objects.filter(pedidoFarmacia__pk=id_pedido).latest("id")
        detallesRemito = models.DetalleRemitoDeFarmacia.objects.filter(remito=remito)
        return super(remitoFarmacia, self).get_context_data(
            pagesize="A4",
            remito= remito,
            detallesRemito = detallesRemito
        )

# ******************************* PEDIDOS DE CLINICA ******************************* #

@login_required(login_url='login')
def pedidosDeClinica(request):
    mfilters = get_filtros(request.GET, models.PedidoDeClinica)
    pedidos = models.PedidoDeClinica.objects.filter(**mfilters)
    return render(request, "pedidoDeClinica/pedidos.html", {"pedidos": pedidos, "filtros": request.GET})

@login_required(login_url='login')
def pedidoDeClinica_add(request):
    limpiar_sesion("pedidoDeClinica", "detallesPedidoDeClinica", request.session)
    if request.method == "POST":
        form = forms.PedidoDeClinicaForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido_json = pedido.to_json()
            pedido_json['nroPedido'] = get_next_nro_pedido(models.PedidoDeClinica, "nroPedido")
            request.session["pedidoDeClinica"] = pedido_json
            return redirect('detallesPedidoDeClinica')
    else:
           form = forms.PedidoDeClinicaForm()
    return render(request, "pedidoDeClinica/pedidoAdd.html", {"form": form})

@login_required(login_url='login')
def pedidoDeClinica_ver(request, id_pedido):
    pedido = get_object_or_404(models.PedidoDeClinica,pk=id_pedido)
    detalles = models.DetallePedidoDeClinica.objects.filter(pedidoDeClinica=pedido)
    return render(request, "pedidoDeClinica/pedidoVer.html",{"pedido": pedido, "detalles": detalles})

@json_view
@login_required(login_url='login')
def pedidoDeClinica_registrar(request):
    pedido = request.session["pedidoDeClinica"]
    detalles = request.session["detallesPedidoDeClinica"]
    mensaje_error = None
    if detalles:
        clinica = get_object_or_404(Clinica, pk=pedido['clinica']['id'])
        fecha = datetime.datetime.strptime(pedido['fecha'], '%d/%m/%Y').date()
        obraSocial = pedido['obraSocial']
        medicoAuditor = pedido['medicoAuditor']
        if not(models.PedidoDeClinica.objects.filter(pk=pedido["nroPedido"]).exists()):
            p = models.PedidoDeClinica(clinica=clinica, fecha=fecha, obraSocial=obraSocial, medicoAuditor=medicoAuditor)
            p.save()
            for detalle in detalles:
                medicamento = get_object_or_404(Medicamento, pk=detalle['medicamento']['id'])
                d = models.DetallePedidoDeClinica(pedidoDeClinica=p, medicamento=medicamento, cantidad=detalle['cantidad'])
                d.save()
            utils.procesar_pedido_de_clinica(p)
            existeRemito = p.estado != "Pendiente"
            return {'success': True, 'existeRemito': existeRemito}
        else:
            mensaje_error = "El pedido ya Existe!"
    else:
        mensaje_error = "No se puede registrar un pedido sin detalles"
    return {'success': False, 'mensaje-error': mensaje_error}


@login_required(login_url='login')
def detallesPedidoDeClinica(request):
    #del request.session['detalles']
    detalles = request.session.setdefault("detallesPedidoDeClinica", [])
    pedido = request.session["pedidoDeClinica"]
    print request.session["pedidoDeClinica"]
    return render(request, "pedidoDeClinica/detallesPedido.html", {'pedido': pedido, 'detalles': detalles})


@json_view
@login_required(login_url='login')
def detallePedidoDeClinica_add(request):
    success = True
    form = forms.DetallePedidoDeClinicaForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            det = form.save(commit=False)
            detalles = request.session["detallesPedidoDeClinica"]
            if not existe_medicamento_en_pedido(detalles, det.medicamento.id):
                detalles.append(crear_detalle_json(det, len(detalles) + 1))
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
@login_required(login_url='login')
def detallePedidoDeClinica_delete(request, id_detalle):
    detalles = request.session['detallesPedidoDeClinica']
    del detalles[int(id_detalle) - 1]
    for i in range(0, len(detalles)):
        detalles[i]['renglon'] = i + 1
    request.session['detallesPedidoDeClinica'] = detalles
    return {'detalles': detalles}


#=================VISTAS DE PEDIDO A LABORATORIO NUEVAS=================#

def get_detalles_a_pedir(pkLaboratorio):
    detalles_a_pedir = []
    #pedidos pendientes y parcialmente enviado
    pedidos = models.PedidoDeFarmacia.objects.filter( Q(estado = 'Pendiente')|Q(estado = 'Parcialmente Enviado') )
    
    for pedido in pedidos:
        detalles = models.DetallePedidoDeFarmacia.objects.filter( Q(pedidoDeFarmacia = pedido.pk) & Q( estaPedido = False ) & Q(cantidadPendiente__gt = 0)& Q( medicamento__laboratorio = pkLaboratorio ))
        
        for detalle in detalles:
            #creo el detalle del pedido a laboratorio asociado al detalle pedido de farmacia
            detallePedidoAlaboratorio = models.DetallePedidoAlaboratorio()
            detallePedidoAlaboratorio.medicamento = detalle.medicamento
            detallePedidoAlaboratorio.cantidad = detalle.cantidadPendiente 
            detallePedidoAlaboratorio_json = detallePedidoAlaboratorio.to_json()
            detallePedidoAlaboratorio_json['detallePedidoFarmacia'] = detalle.id
            detalles_a_pedir.append(detallePedidoAlaboratorio_json)
    return detalles_a_pedir

@login_required(login_url='login')
def pedidosAlaboratorio(request):
    filters = get_filtros(request.GET, models.PedidoAlaboratorio)
    mfilters = dict(filter(lambda v: v[0] in models.PedidoAlaboratorio.FILTROS, filters.items()))
    pedidosAlab = models.PedidoAlaboratorio.objects.filter(**mfilters)
    return render(request, "pedidoAlaboratorio/pedidos.html", {"pedidosAlab": pedidosAlab, "filtros": filters})

@login_required(login_url='login')
def pedidoAlaboratorio_add(request):
    limpiar_sesion('pedidoAlaboratorio', 'detallesPedidoAlaboratorio', request.session)
    if request.method == 'POST': 
        form = forms.PedidoLaboratorioForm(request.POST); 
        if form.is_valid():
            pedido = form.save(commit = False)
            pedido_json = pedido.to_json()
            pedido_json['numero'] = get_next_nro_pedido_laboratorio(models.PedidoAlaboratorio, "numero")
            request.session['pedidoAlaboratorio'] = pedido_json
            request.session['detallesPedidoAlaboratorio'] = get_detalles_a_pedir(pedido_json['laboratorio']['id'])
            return redirect('detallesPedidoAlaboratorio')
    else:
        form = forms.PedidoLaboratorioForm()
    return render(request, 'pedidoAlaboratorio/pedidoAdd.html', {'form': form})

def pedidoAlaboratorio_ver(request, id_pedido):
    pedidoALab = get_object_or_404(models.PedidoAlaboratorio, pk=id_pedido)
    detalles = models.DetallePedidoAlaboratorio.objects.filter(pedido=pedidoALab.numero)
    return render(request, "pedidoAlaboratorio/pedidoVer.html", {'nombreLab': pedidoALab.laboratorio.razonSocial, 'numeroPedido': pedidoALab.pk, 'fecha':pedidoALab.fecha, 'detalles': detalles})

def detallesPedidoAlaboratorio(request):
    pedido = request.session['pedidoAlaboratorio']
    detalles = request.session["detallesPedidoAlaboratorio"]
    return render(request, "pedidoAlaboratorio/detallesPedido.html", {'pedido': pedido, 'detalles': detalles})

@json_view
@login_required(login_url='login')
def detallePedidoAlaboratorio_add(request):
    success = True #paso 1
    id_laboratorio = request.session['pedidoAlaboratorio']['laboratorio']['id'] #paso 2
    if request.method == 'POST': #paso 3
        form = forms.DetallePedidoAlaboratorioFormFactory(id_laboratorio)(request.POST) #paso 4
        if form.is_valid(): #paso 5
            det = form.save(commit=False) #paso 6
            detalles = request.session["detallesPedidoAlaboratorio"] #paso 7
            detallePedidoAlaboratorio_json = det.to_json() #paso 8
            #detalle suelto no se corresponde con ningun detalle de pedido de farmacia
            detallePedidoAlaboratorio_json['detallePedidoFarmacia'] = -1 #paso 9
            detalles.append(detallePedidoAlaboratorio_json) #paso 10
            request.session["detallesPedidoAlaboratorio"] = detalles #paso 11
            #Nuevo form para seguir dando de alta
            form = forms.DetallePedidoAlaboratorioFormFactory(id_laboratorio)() #paso 12

            form_html = render_crispy_form(form, context=RequestContext(request)) #paso 13
            return {'success': success, 'form_html': form_html, 'detalles': detalles} #paso 14
        else: #paso 15
            success = False #paso 16
    else: #paso 17
        form = forms.DetallePedidoAlaboratorioFormFactory(id_laboratorio)() #paso 18
    form_html = render_crispy_form(form, context=RequestContext(request)) #paso 19
    return {'success': success, 'form_html': form_html} #paso 20

@json_view
@login_required(login_url='login')
def pedidoAlaboratorio_registrar(request):
    pedido = request.session['pedidoAlaboratorio'] #paso 1
    detalles = request.session['detallesPedidoAlaboratorio'] #paso 2
    mensaje_error = None #paso 3
    if detalles: #paso 4
        laboratorio = get_object_or_404(Laboratorio, pk=pedido['laboratorio']['id']) #paso 5
        fecha = datetime.datetime.strptime(pedido['fecha'], '%d/%m/%Y').date() #paso 6
        if not(models.PedidoAlaboratorio.objects.filter(pk=pedido["numero"]).exists()): #paso 7
            p = models.PedidoAlaboratorio(laboratorio=laboratorio, fecha=fecha)#paso 8
            p.save() #paso 9
            for detalle in detalles: #paso 10
                medicamento = get_object_or_404(Medicamento, pk=detalle['medicamento']['id']) #paso 11
                d = models.DetallePedidoAlaboratorio(pedido=p, medicamento=medicamento, cantidad=detalle['cantidad'], cantidadPendiente=detalle['cantidad']) #paso 12
                if detalle['detallePedidoFarmacia'] != -1: #paso 13
                    detallePedidoFarmacia = get_object_or_404(models.DetallePedidoDeFarmacia, pk=detalle['detallePedidoFarmacia']) #paso 14
                    detallePedidoFarmacia.estaPedido = True #paso 15
                    detallePedidoFarmacia.save() #paso 16
                    d.detallePedidoFarmacia =  detallePedidoFarmacia #paso 17
                d.save() #paso 18
            return {'success': True} #paso 19
        else: #paso 20
            mensaje_error = "El pedido ya Existe!" #paso 21
    else: #paso 22
        mensaje_error = "No se puede registrar un pedido sin detalles" #paso 23
    return {'success': False, 'mensaje-error': mensaje_error} #paso 24

#========================================INICIO RECEPCION DE PEDIDO A LABORATORIO====================================================

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

def get_pos_detalle(detalles, id_detalle):
    i = 0
    for detalle in detalles:
        if detalle['renglon'] == id_detalle:
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

    if numeroLote in recepcionPedidoAlaboratorio['nuevosLotes']:
        lote = recepcionPedidoAlaboratorio['nuevosLotes'][numeroLote]
        lote['stock'] += infoRecepcionDetalle['cantidad']
        recepcionPedidoAlaboratorio['nuevosLotes'][numeroLote] = lote # guardo cambios
    else:
        if numeroLote in recepcionPedidoAlaboratorio['actualizarLotes']:
            lote = recepcionPedidoAlaboratorio['actualizarLotes'][numeroLote]
            lote += infoRecepcionDetalle['cantidad']
            recepcionPedidoAlaboratorio['actualizarLotes'][numeroLote] = lote # guardo cambios
        else:
            recepcionPedidoAlaboratorio['actualizarLotes'][numeroLote] = infoRecepcionDetalle['cantidad']

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
    nuevoLote = {
        'fechaVencimiento': infoRecepcionDetalle['fechaVencimiento'].strftime('%d/%m/%Y'),
        'precio': infoRecepcionDetalle['precio'],
        'stock': infoRecepcionDetalle['cantidad'],
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
        lote = Lote()
        lote.numero = numeroLote
        lote.fechaVencimiento = datetime.datetime.strptime(info['fechaVencimiento'], '%d/%m/%Y').date()
        lote.precio = info['precio']
        lote.stock = info['stock']
        lote.medicamento = get_object_or_404(Medicamento, pk=info['medicamento'])
        lote.save()        

def actualizar_lotes(lotes):
    for numeroLote, cantidadRecibida in lotes.items():
        lote = get_object_or_404(Lote, numero=numeroLote)
        lote.stock += cantidadRecibida
        lote.save()

def actualizar_pedido(pedido, detalles):
    recepcionDelPedidoCompleta = True
    for detalle in detalles:
        if detalle['actualizado']:
            detalleDb = get_object_or_404(models.DetallePedidoAlaboratorio, pk=detalle['renglon'])
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

@login_required(login_url='login')
def recepcionPedidoAlaboratorio(request):
    mfilters = get_filtros(request.GET, models.PedidoAlaboratorio)
    pedidos = models.PedidoAlaboratorio.objects.filter(**mfilters)
    fecha = datetime.datetime.now()
    recibidos = pedidos.filter( Q(estado = 'Pendiente')|Q(estado = 'Parcialmente Recibido') )
    return render(request, "recepcionPedidoALaboratorio/pedidos.html", {'recibidos': recibidos,'fecha':fecha, "filtros": request.GET})

@login_required(login_url='login')
def recepcionPedidoAlaboratorio_cargarPedido(request, id_pedido):
    limpiar_sesion('recepcionPedidoAlaboratorio', 'remitoRecepcion', request.session)
    cargar_detalles(id_pedido, request.session)
    request.session['remitoRecepcion'] = {'remito':{}, 'detalles':[]}
    return redirect('recepcionPedidoAlaboratorio_registrarRecepcion', id_pedido)

@login_required(login_url='login')
def recepcionPedidoAlaboratorio_controlPedido(request, id_pedido):
    pedido = get_object_or_404(models.PedidoAlaboratorio, pk=id_pedido)
    detalles = request.session['recepcionPedidoAlaboratorio']['detalles']

    print request.session['remitoRecepcion']


    return render(request, "recepcionPedidoALaboratorio/controlPedido.html", {'pedido': pedido, 'detalles': detalles})

@login_required(login_url='login')
def recepcionPedidoAlaboratorio_registrarRecepcion(request, id_pedido):
    if request.method == 'POST':
        form = forms.RegistrarRecepcionForm(request.POST)
        if form.is_valid():
            nroRemito = form.cleaned_data['nroRemito']
            fecha = form.cleaned_data['fechaRemito']
            fecha = fecha.strftime('%d/%m/%Y')
            info = {'remito':{'nroRemito':nroRemito, 'fecha':fecha},'detalles':[]}
            request.session['remitoRecepcion'] = info

            return redirect('recepcionPedidoAlaboratorio_controlPedido', id_pedido)
    else:
        form=forms.RegistrarRecepcionForm()
        form.helper.form_action = reverse('recepcionPedidoAlaboratorio_registrarRecepcion', args=[id_pedido])

    return render(request, "recepcionPedidoALaboratorio/registrarRemito.html", {'form': form})


@login_required(login_url='login')
def recepcionPedidoAlaboratorio_controlDetalle(request, id_pedido, id_detalle):
    if hay_cantidad_pendiente(request.session['recepcionPedidoAlaboratorio']['detalles'], id_detalle):
        pedido = get_object_or_404(models.PedidoAlaboratorio, pk = id_pedido)
        detalle = get_object_or_404(models.DetallePedidoAlaboratorio, pk = id_detalle)
        lotesEnSesion = request.session['recepcionPedidoAlaboratorio']['nuevosLotes']
        if request.method == 'POST':
            form = forms.ControlDetallePedidoAlaboratorioFormFactory(detalle.medicamento.id, lotesEnSesion)(request.POST)
            posDetalle = get_pos_detalle(request.session['recepcionPedidoAlaboratorio']['detalles'], detalle.renglon)
            infoDetalle = request.session['recepcionPedidoAlaboratorio']['detalles'][posDetalle]
            if form.is_valid(infoDetalle['cantidadPendiente']):
                guardar_recepcion_detalle(request.session, detalle, form.clean())
                if '_volver' in request.POST:
                    return redirect('recepcionPedidoAlaboratorio_controlPedido', pedido.numero)
                else:
                    return redirect('recepcionPedidoAlaboratorio_controlDetalle', pedido.numero, detalle.renglon)
        else:
            if not medicamento_tiene_lotes(detalle.medicamento, request.session['recepcionPedidoAlaboratorio']['nuevosLotes']):
                return redirect('recepcionPedidoAlaboratorio_controlDetalleConNuevoLote', pedido.numero, detalle.renglon)
            form = forms.ControlDetallePedidoAlaboratorioFormFactory(detalle.medicamento.id, lotesEnSesion)()
            form.helper.form_action = reverse('recepcionPedidoAlaboratorio_controlDetalle', args=[pedido.numero, detalle.renglon])
        return render(request, "recepcionPedidoALaboratorio/controlDetalle.html", {'btnNuevoLote': True, 'pedido': pedido, 'detalle': detalle, 'form': form})
    else:
        return redirect('recepcionPedidoAlaboratorio_controlPedido', id_pedido)

@login_required(login_url='login')
def recepcionPedidoAlaboratorio_controlDetalleConNuevoLote(request, id_pedido, id_detalle):
    if hay_cantidad_pendiente(request.session['recepcionPedidoAlaboratorio']['detalles'], id_detalle):
        pedido = get_object_or_404(models.PedidoAlaboratorio, pk = id_pedido)
        detalle = get_object_or_404(models.DetallePedidoAlaboratorio, pk = id_detalle)
        if request.method == 'POST':
            form = forms.ControlDetalleConNuevoLotePedidoAlaboratorioForm(request.POST)
            posDetalle = get_pos_detalle(request.session['recepcionPedidoAlaboratorio']['detalles'], detalle.renglon)
            infoDetalle = request.session['recepcionPedidoAlaboratorio']['detalles'][posDetalle]
            if form.is_valid(infoDetalle['cantidadPendiente'], request.session['recepcionPedidoAlaboratorio']['nuevosLotes']):
                guardar_recepcion_detalle_con_nuevo_lote(request.session, detalle, form.clean())
                if '_volver' in request.POST:
                    return redirect('recepcionPedidoAlaboratorio_controlPedido', pedido.numero)
                else:
                    return redirect('recepcionPedidoAlaboratorio_controlDetalleConNuevoLote', pedido.numero, detalle.renglon)
        else:       
            form = forms.ControlDetalleConNuevoLotePedidoAlaboratorioForm()
            form.helper.form_action = reverse('recepcionPedidoAlaboratorio_controlDetalleConNuevoLote', args=[pedido.numero, detalle.renglon])
        existenLotes = False
        if medicamento_tiene_lotes(detalle.medicamento, request.session['recepcionPedidoAlaboratorio']['nuevosLotes']):
            existenLotes = True
        return render(request, "recepcionPedidoALaboratorio/controlDetalle.html", {'btnNuevoLote': False, 'existenLotes': existenLotes, 'pedido': pedido, 'detalle': detalle, 'form': form})
    else:
        return redirect('recepcionPedidoAlaboratorio_controlPedido', id_pedido)


def procesar_recepcion(sesion, pedido):

    remitoSesion = sesion['remitoRecepcion']['remito']
    detalleRemitoSesion = sesion['remitoRecepcion']['detalles']
    nuevosLotes = sesion['recepcionPedidoAlaboratorio']['nuevosLotes']
    actualizarLotes = sesion['recepcionPedidoAlaboratorio']['actualizarLotes']
    detalles = sesion['recepcionPedidoAlaboratorio']['detalles']

    crear_nuevos_lotes(nuevosLotes)
    actualizar_lotes(actualizarLotes)
    actualizar_pedido(pedido, detalles)

    remito = models.RemitoLaboratorio()
    remito.nroRemito = remitoSesion['nroRemito']
    remito.fecha= datetime.datetime.strptime(remitoSesion['fecha'], '%d/%m/%Y').date()
    remito.laboratorio = pedido.laboratorio
    remito.pedidoLaboratorio = pedido
    remito.save()

    for detalle in detalleRemitoSesion:

        detalleRemito = models.DetalleRemitoLaboratorio()
        detalleRemito.remito = remito
        detalleRemito.cantidad = detalle['cantidad']
        detalleRemito.lote  = get_object_or_404(mmodels.Lote, pk= detalle['lote'])
        detalleRemito.detallePedidoLaboratorio = get_object_or_404(models.DetallePedidoAlaboratorio, pk= detalle['detallePedidoLaboratorio'])
        detalleRemito.save()




@login_required(login_url='login')
def recepcionPedidoAlaboratorio_registrar(request, id_pedido):
    pedido = get_object_or_404(models.PedidoAlaboratorio, pk=id_pedido)
    detalles = request.session['recepcionPedidoAlaboratorio']['detalles']
    nuevosLotes = request.session['recepcionPedidoAlaboratorio']['nuevosLotes']
    actualizarLotes = request.session['recepcionPedidoAlaboratorio']['actualizarLotes']


    if len(nuevosLotes) > 0 or len(actualizarLotes) > 0:

        procesar_recepcion(request.session,pedido)

        return render(request, "recepcionPedidoALaboratorio/controlPedido.html", {'pedido': pedido, 'detalles': detalles, 'modalSuccess': True})

    return render(request, "recepcionPedidoALaboratorio/controlPedido.html", {'pedido': pedido, 'detalles': detalles, 'modalError': True})

@login_required(login_url='login')
def devolucionMedicamentosVencidos(request):

    if request.method =='POST':
        form = forms.DevolucionMedicamentosForm(request.POST)
        if form.is_valid():
            formLaboratorio= form.cleaned_data.get('laboratorio')
            return redirect('devolucionMedicamentosVencidos_detalle', formLaboratorio.id)
    else:
        form = forms.DevolucionMedicamentosForm()
    return render(request, "devolucionMedicamentosVencidos/devolucionMedicamentosVencidos.html", {'form':form})


@login_required(login_url='login')
def devolucionMedicamentosVencidos_detalle(request, id_laboratorio):

    laboratorio = get_object_or_404(omodels.Laboratorio, pk=id_laboratorio)
    medicamentos = Medicamento.objects.filter(laboratorio = laboratorio) # todos los medicamentos
    lista = []

    for m in medicamentos:
        lista.append(m.pk)

    lt =datetime.date.today() + datetime.timedelta(weeks=26) # fecha vencimiento.(limite)
    lotes = Lote.objects.filter(fechaVencimiento__lte = lt, medicamento__pk__in = lista, stock__gt=0)


    return render(request,"devolucionMedicamentosVencidos/devolucionMedicamentosVencidos_detalle.html", {'lotes':lotes, 'laboratorio':laboratorio} )


@login_required(login_url='login')
def devolucionMedicamentosVencidos_registrar(request, id_laboratorio):

    laboratorio = get_object_or_404(omodels.Laboratorio, pk=id_laboratorio)
    medicamentos = Medicamento.objects.filter(laboratorio = laboratorio) # todos los medicamentos
    lista = []

    for m in medicamentos:
        lista.append(m.pk)

    lt =datetime.date.today() + datetime.timedelta(weeks=26) # fecha vencimiento.(limite)
    lotes = Lote.objects.filter(fechaVencimiento__lte = lt, medicamento__pk__in = lista, stock__gt=0)

    for l in lotes:
        l.stock=0
        l.save()

    return redirect("inicio")