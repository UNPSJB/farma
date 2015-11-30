from django.shortcuts import render, redirect, get_object_or_404, RequestContext
from jsonview.decorators import json_view
from pedidos import forms, models, utils
from organizaciones.models import Farmacia, Clinica
from django.contrib.auth.decorators import login_required
from crispy_forms.utils import render_crispy_form
from django.contrib.auth import decorators as authd
from medicamentos.models import Medicamento
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

def get_next_nro_pedido(m):
    nro = None
    try:
        nro = m.objects.latest("nroPedido").nroPedido + 1
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
def pedidoF_add(request):
    limpiar_sesion("pedidoDeFarmacia", "detallesPedidoDeFarmacia", request.session)
    if request.method == "POST":
        form = forms.PedidoDeFarmaciaForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido_json = pedido.to_json()
            pedido_json['nroPedido'] = get_next_nro_pedido(models.PedidoDeFarmacia)
            request.session['pedidoDeFarmacia'] = pedido_json
            return redirect('detalles_pedidoF')
    else:
           form = forms.PedidoDeFarmaciaForm()
    return render(request, "pedidoDeFarmacia/pedidoAdd.html", {"form": form})

#PEDIDO DE FARMACIA#
@login_required(login_url='login')
def detalles_pedidoF(request):
    #del request.session['detalles']
    detalles = request.session.setdefault("detallesPedidoDeFarmacia", [])
    pedido = request.session['pedidoDeFarmacia']
    return render(request, "pedidoDeFarmacia/pedido-detalles.html", {'pedido': pedido, 'detalles': detalles})

@login_required(login_url='login')
def ver_pedidoF(request, id_pedido):
    pedido = get_object_or_404(models.PedidoDeFarmacia,pk=id_pedido)
    detalles = models.DetallePedidoDeFarmacia.objects.filter(pedidoDeFarmacia=pedido)
    return render(request, "pedidoDeFarmacia/ver-pedido.html",{"pedido": pedido, "detalles": detalles})

@json_view
@login_required(login_url='login')
def add_detalle_pedido_farmacia(request):
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
def update_detalle_pedido_farmacia(request, id_detalle):
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
def delete_detalle_pedido_farmacia(request, id_detalle):
    detalles = request.session['detallesPedidoDeFarmacia']
    del detalles[int(id_detalle) - 1]
    for i in range(0, len(detalles)):
        detalles[i]['renglon'] = i + 1
    request.session['detallesPedidoDeFarmacia'] = detalles
    return {'detalles': detalles}

#https://github.com/incuna/django-wkhtmltopdf !!!!!!!!!!!!!!!
@json_view
@login_required(login_url='login')
@authd.permission_required(perm="add_pedidodefarmacia")
@authd.permission_required(perm="change_pedidodefarmacia")
def registrar_pedido_farmacia(request):
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
            utils.procesar_pedido_de_farmacia(p)
            return {'success': True}
        else:
            mensaje_error = "El pedido ya Existe!"
    else:
        mensaje_error = "No se puede registrar un pedido sin detalles"
    return {'success': False, 'mensaje-error': mensaje_error}


# ******************************* PEDIDOS DE CLINICA ******************************* #

@login_required(login_url='login')
def pedidosDeClinica(request):
    mfilters = get_filtros(request.GET, models.PedidoDeClinica)
    pedidos = models.PedidoDeClinica.objects.filter(**mfilters)
    return render(request, "pedidoDeClinica/pedidos.html", {"pedidos": pedidos, "filtros": request.GET})

@login_required(login_url='login')
def pedido_de_clinica_add(request):
    limpiar_sesion("pedidoDeClinica", "detallesPedidoDeClinica", request.session)
    if request.method == "POST":
        form = forms.PedidoDeClinicaForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido_json = pedido.to_json()
            pedido_json['nroPedido'] = get_next_nro_pedido(models.PedidoDeClinica)
            request.session["pedidoDeClinica"] = pedido_json
            return redirect('pedido_de_clinica_detalles')
    else:
           form = forms.PedidoDeClinicaForm()
    return render(request, "pedidoDeClinica/pedidoAdd.html", {"form": form})

@login_required(login_url='login')
def pedido_de_clinica_detalles(request):
    #del request.session['detalles']
    detalles = request.session.setdefault("detallesPedidoDeClinica", [])
    pedido = request.session["pedidoDeClinica"]
    print request.session["pedidoDeClinica"]
    return render(request, "pedidoDeClinica/pedido-detalles.html", {'pedido': pedido, 'detalles': detalles})

@login_required(login_url='login')
def ver_pedido_de_clinica(request, id_pedido):
    pedido = get_object_or_404(models.PedidoDeClinica,pk=id_pedido)
    detalles = models.DetallePedidoDeClinica.objects.filter(pedidoDeClinica=pedido)
    return render(request, "pedidoDeClinica/ver-pedido.html",{"pedido": pedido, "detalles": detalles})

@json_view
@login_required(login_url='login')
def add_detalle_pedido_de_clinica(request):
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
def update_detalle_pedido_de_clinica(request, id_detalle):
    detalles = request.session['detallesPedidoDeClinica']
    detalle = models.DetallePedidoDeClinica(cantidad=detalles[int(id_detalle) - 1]['cantidad'])
    if request.method == "POST":
        form = forms.UpdateDetallePedidoDeClinicaForm(request.POST, instance=detalle)
        if form.is_valid():
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
def delete_detalle_pedido_de_clinica(request, id_detalle):
    detalles = request.session['detallesPedidoDeClinica']
    del detalles[int(id_detalle) - 1]
    for i in range(0, len(detalles)):
        detalles[i]['renglon'] = i + 1
    request.session['detallesPedidoDeClinica'] = detalles
    return {'detalles': detalles}

#https://github.com/incuna/django-wkhtmltopdf !!!!!!!!!!!!!!!
@json_view
@login_required(login_url='login')
def registrar_pedido_de_clinica(request):
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
            return {'success': True}
        else:
            mensaje_error = "El pedido ya Existe!"
    else:
        mensaje_error = "No se puede registrar un pedido sin detalles"
    return {'success': False, 'mensaje-error': mensaje_error}
