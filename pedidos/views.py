#!/usr/bin/python
# -*- encoding: utf-8 -*-
from easy_pdf.views import PDFTemplateView
from django.db.models import Q # Herramienta que nos permite "darle de comer" expresiones con OR a los filter

from medicamentos import models as mmodels
from organizaciones import models as omodels

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404, RequestContext
from jsonview.decorators import json_view
from pedidos import forms, models, utils
from organizaciones.models import Farmacia, Clinica, Laboratorio
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
    return render(request, "pedidoDeFarmacia/pedidoVer.html",{"pedido": pedido, "detalles": detalles})


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
            return {'success': True}
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
            #utils.procesar_pedido_de_clinica(p)
            return {'success': True}
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
def detallePedidoDeClinica_delete(request, id_detalle):
    detalles = request.session['detallesPedidoDeClinica']
    del detalles[int(id_detalle) - 1]
    for i in range(0, len(detalles)):
        detalles[i]['renglon'] = i + 1
    request.session['detallesPedidoDeClinica'] = detalles
    return {'detalles': detalles}


#=================VISTAS DE PEDIDO A LABORATORIO NUEVAS=================#

"""""
Descripción: 
    Se encarga de recuperar todos los detalles (de los Pedidos de Farmacia) que van
    a formar parte del pedido a laboratorio. Y los devuelve en un arreglo.

Cada uno de los detalles debe cumplir las siguientes condiciones:
    * debe pertenecer a un pedido de farmacia con el estado "pendiente" o "parcialmente enviado".
    * debe tener el campo "estaPedido" en False.
    * el detalle de pedido de farmacia debe contener un medicamento producido por el laboratorio
      al cual se le está realizando el pedido.

"""""
def get_detalles_a_pedir(pkLaboratorio):
    detalles_a_pedir = []
    #pedidos pendientes y parcialmente enviado
    pedidos = models.PedidoDeFarmacia.objects.filter( Q(estado = 'Pendiente')|Q(estado = 'Parcialmente Enviado') )
    
    for pedido in pedidos:
        detalles = models.DetallePedidoDeFarmacia.objects.filter( Q(pedidoDeFarmacia=pedido.pk) & Q( estaPedido=False ) & Q( medicamento__laboratorio=pkLaboratorio ))
        
        for detalle in detalles:
            #creo el detalle del pedido a laboratorio asociado al detalle pedido de farmacia
            detallePedidoAlaboratorio = models.DetallePedidoAlaboratorio()
            detallePedidoAlaboratorio.medicamento = detalle.medicamento
            detallePedidoAlaboratorio.cantidad = detalle.cantidadPendiente 
            detallePedidoAlaboratorio_json = detallePedidoAlaboratorio.to_json()
            detallePedidoAlaboratorio_json['detallePedidoFarmacia'] = detalle.id
            detalles_a_pedir.append(detallePedidoAlaboratorio_json)
    return detalles_a_pedir
    

"""""
Descripción: 
    Vista que se encarga de procesar los filtros y mostrar todos los pedidos a
    laboratorio que se encuentran efectuados.
"""""
@login_required(login_url='login')
def pedidosAlaboratorio(request):
    filters = get_filtros(request.GET, models.PedidoAlaboratorio)
    mfilters = dict(filter(lambda v: v[0] in models.PedidoAlaboratorio.FILTROS, filters.items()))
    pedidosAlab = models.PedidoAlaboratorio.objects.filter(**mfilters)
    return render(request, "pedidoAlaboratorio/pedidos.html", {"pedidosAlab": pedidosAlab, "filtros": filters})


"""""
Descripción: Vista que se encarga de mostrar y procesar el formulario de alta de un pedido
a laboratorio.

Explicación:
    paso 1: limpia la sesión anterior para empezar un nuevo pedido a laboratorio.
    paso 2: Si request viene por "POST" (Se presionó el botón continuar).
    paso 3: Valida que el formulario no contenga errores(campos incompletos, datos erroneos, etc).
    paso 4: Crea una instancia de PedidoAlaboratorio con los datos del formulario.
    paso 5: El método to_json está implementado en la clase PedidoAlaboratorio (models.py).
            Lo que hace este método es devolver la información de la instancia de pedido a 
            laboratorio en formato json. Específicamente devuelve el laboratorio(con su id 
            y razón social) y la fecha actual en la que se esta creando este pedido.
            Dicha información la guarda en la variable pedido_json.
    paso 6: Agrega un nuevo campo a la variable pedido_json llamada "numero" y le asigna el
            próximo número pedido a laboratorio.
    paso 7: Guarda en la sesión el objeto en formato json con toda la información del pedido a
            laboratorio.
    paso 8: Guarda en la sesión todos los detalles de pedido a laboratorio(solo los que se
            corresponden a pedidos de farmacia).
    paso 9: Se redirige a la siguiente página.
    paso 10: Si entra en este "else" es porque el método del request es GET.
    paso 11: Se crea un formulario vacio
    paso 12: Renderiza nuevamente la página
    
"""""
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

"""
Descripción:
    Vista que se encarga de mostrar el pedido a laboratorio y todos sus detalles.
"""
def pedidoAlaboratorio_ver(request, id_pedido):
    pedidoALab = get_object_or_404(models.PedidoAlaboratorio, pk=id_pedido)
    detalles=models.DetallePedidoAlaboratorio.objects.filter(pedido=pedidoALab.numero)
    return render(request, "pedidoAlaboratorio/pedidoVer.html", {'nombreLab': pedidoALab.laboratorio.razonSocial, 'numeroPedido': pedidoALab.pk, 'fecha':pedidoALab.fecha, 'detalles': detalles})


"""
Descripción:
    Vista que se encarga de mostrar el pedido a laboratorio y sus detalles (ambos los recupera
    de la sesión).
"""
def detallesPedidoAlaboratorio(request):
    pedido = request.session['pedidoAlaboratorio']
    detalles = request.session["detallesPedidoAlaboratorio"]
    return render(request, "pedidoAlaboratorio/detallesPedido.html", {'pedido': pedido, 'detalles': detalles})


"""
Descripción:
    Vista que se encarga de manejar el alta de un detalle de pedido a laboratorio (suelto).
    
Explicación:
    paso 1: Declara la variable "success" y le asigna el valor por defecto True. Esta variable
            sirve para controlar si el alta de un detalle se realizó exitosamente o no.
    paso 2: Recupera la id del laboratorio a la que se le está realizando este pedido.
    paso 3: Si request viene por "POST" (Se presionó el botón Guardar del modal).
    paso 4: Crea un formulario de detalle pedido a laboratorio con la información que vino por POST.
    paso 5: Valida que el formulario no contenga errores(campos incompletos, datos erroneos, etc).
    paso 6: Crea una instancia de DetallePedidoAlaboratorio con los datos del formulario.
    paso 7: Recupera todos los detalles de pedido a laboratorio guardados en la sesión.
    paso 8: El método to_json está implementado en la clase DetallePedidoAlaboratorio (models.py).
            Lo que hace este método es devolver la información de la instancia del detalle pedido
            a laboratorio en formato json. Específicamente devuelve el medicamento(con su id 
            y una descripción) y la cantidad a pedir.
            Dicha información la guarda en la variable detallePedidoAlaboratorio_json.
    paso 9: Agrega un nuevo campo a la variable detallePedidoAlaboratorio_json llamada 
            "detallePedidoAlaboratorio" y le asigna -1. El -1 es una marca que sirve para 
            indicar que este detalle de pedido a laboratorio no esta relacionado con ningún
            detalle de pedido de farmacia, sino que es un detalle "suelto".
    paso 10: Agregar el nuevo detalle creado al arreglo de detalles.
    paso 11: Setea el nuevo arreglo de detalles a la sesión.
    paso 12: Se crea un nuevo formulario de DetallePedidoAlaboratorio para que el usuario
             pueda seguir creando detalles sin necesidad de cerrar y abrir nuevamente el modal.
             Cuando un detalle se da de alta exitosamente, el modal muestra este nuevo formulario
             vacio.
    paso 13: La función render_crispy_form, transforma el objeto form y lo convierte en código html. 
             Esto sirve para que cuando se reciba la respuesta de ésta vista, del lado del
             cliente (con javascript), se agarre el formulario y directamente se "setee" en la pagina.
             Con setear me refiero a, seleccionar la parte de la página en la que se encuentra el código 
             HTML del formulario viejo y reemplazarlo con este nuevo código HTML del nuevo formulario.
    paso 14: Retorna un objeto json con la información correspondiente. En este caso "success" es True
             porque se pudo dar de alta un nuevo detalle, "form_html" es el código HTML de un nuevo 
             formulario vacío (para que el usuario pueda seguir agregando detalles) y detalles son 
             todos los detalles del pedido a laboratorio que se van a volver a recargar utilizando 
             javscript("se borran todos las filas de la tabla y se las vuelven a crear").
    paso 15: Si entra por éste "else" entonces el formulario no es valido.
    paso 16: Se le asigna a la variable "success" el valor de False para indicar que hubo un error
             al tratar de dar de alta el detalle (datos del form incorrectos).
    paso 17: Si entra por éste "else" entonces el request viene por "GET".
    paso 18: Se crear un formulario de DetallePedidoAlaboratorio nuevo.
    paso 19: Nuevamente se utiliza la función render_crispy_form para transformar el objeto form
             a su correspondiente a código HTML. En este caso se va a crear el código HTML de un 
             formulario nuevo (si request vino por "GET") o se crea el código HTML de un formulario
             que vino por "POST" pero que el mismo no fhaya sido válido (es decir, se vuelve a crear el mismo
             formulario con la misma información pero además se le agregan todos los errores que deben 
             mostrarse).
    paso 20: Retorna un objecto json con las variables "success" y "form_html".
             Si se llego a este paso porque el request era por "GET" entonces "Success" es True y "form_html"
             es el código HTML de un formulario nuevo y vacio.
             Si se llego a este paso porque request era por "POST" pero el formulario no era válido entonces
             "success" es False y "form_html" es el código HTML del formulario con todos sus errores.
"""
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
 
"""
Descripción:
    Vista que se encarga de registrar pedido a laboratorio con todos sus detalles (los registra en la DB).
    
Explicación:
    paso 1 y paso 2: recupera el pedido a laboratorio y todos sus detalles que se encuentran guardados en la sesión.
    paso 3: "mensaje_error" es una variable que se utliza para poner el texto que se va a mostrar en el caso
            de que ocurra un error al registrar el pedido y sus detalles.
    paso 4: Este if se encarga de comprobar que el arreglo de detalles tenga al menos un detalle, ya que no
            se puede dar de alta un pedido que no tenga detalles.
    paso 5 y 6: Recupera el laboratorio y la fecha del pedido.
    paso 7: Este if se encarga de controlar que el pedido a laboratorio no exista, es decir evita que este
            pedido a laboratorio se registre más de una vez.
    paso 8 y 9: Se crea una instancia de pedido a laboratorio con toda su información y se la da de alta
                en la DB.
    paso 10: Se recorren todos los detalles
    paso 11: Se recupera el medicamento de este detalle
    paso 12: Se crea una instancia de detalle de pedido a laboratorio con toda su información.
    paso 13: Este if comprueba que el detalle de pedido a laboratorio no sea suelto (== -1), en
             caso de no ser un detalle suelto entonces es un detalle de pedido a laboratorio que esta 
             asociado a un detalle de pedido de farmacia.
    paso 14: Se recupera el detalle de pedido de farmacia.
    paso 15: Se marca al detalle de pedido de farmacia como pedido ya que va a formar parte de el actual
             pedido a laboratorio.
    paso 16: Se guarda en la base el detalle de pedido de farmacia para que se efectue el cambio realizado
             en el campo "estaPedido".
    paso 17: Se asocia el detalle pedido a laboratorio con el detalle de pedido de farmacia.
    paso 18: Se guarda el detalle de pedido a laboratorio en la base.
    paso 19: Se devuelve un objeto json con el valor de "success" igual a True ya que el pedido a laboratorio
             y todos sus detalles se pudieron registrar exitosamente.
    paso 20: Si vino por este "else" entonces el pedido a laboratorio ya se había registrado anteriormente.
    paso 21: Setea el mensaje de error correspondiente.
    paso 22: Si vino por este "else" entonces el momento de querer registrar el pedido a laboratorio se 
             detectó que el mismo no tenía detalles.
    paso 23: Setea el mensaje de error correspondiente.
    paso 24: Retorna un objeto json con el valor de "success" igual a False (El pedido ya estaba registrado
             o el pedido no tenía detalles) y el mensaje de error correspondiente.
"""
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






#VISTAS DE PEDIDO A LABORATORIO VIEJAS
##===============================================PEDIDOS A LABORATORIO=================================================
#
#
#@json_view
#@login_required(login_url='login')
#def PedidoLaboratorio_add(request):#metodo que crea un nuevo pedido a laboratorio
#
#    if request.method == "POST": #si el metodo request es por post
#        pedidoALaboratorio_form = forms.PedidoLaboratorioForm(request.POST)#El formulario 'PedidoLaboratorioForm' con los datos actuales del POST
#                                                                           #se guarda en pedidoALaboratorio_form
#
#        if pedidoALaboratorio_form.is_valid():#si los datos en el formulario son validos
#
#            pedido=pedidoALaboratorio_form.save(commit=False)#El pedidoALaboratorio_form se guarda en pedido pero no en la base.
#            request.session["idLab"]=pedido.laboratorio.pk#Se obtiene el id que identifica al laboratorio y se mete en la sesion.
#
#            if '_continuar' in request.POST:#Si el metodo POST trae el valor '_continuar' que pertenece al boton 'crear pedido' debe redirigir a el template 'AgregarRenglonesPedidoLab'
#                return redirect("/pedidoAlaboratorios/agregarRenglones/")
#
#    else: #si no si viene por GET
#        pedidoALaboratorio_form = forms.PedidoLaboratorioForm()#cuando no viene por POST el formulario 'PedidoLaboratorioForm' se guarda en pedidoALaboratorio_form
#        return render(request, 'pedidos_A_laboratorio/PedidoAlaboratorioAdd.html', {"pedidoALaboratorio_form": pedidoALaboratorio_form})#Renderiza el formulario en el template para poder elegir
#
##======================================================================================================================================
#
#@login_required(login_url='login')
#def ListPedidoALaboratorio(request): #Vista "a la que le pega" la url: r'^ListPedidoALaboratorio/$' que luego renderiza la primer
#                                     #pantalla que vemos al comenzar con el proceso de pedidos a laboratorios, en esta pantalla
#                                     #se pueden ver todos los pedidos que se hicieron a laboratorio ,tenemos el acceso
#                                     #para ver estos pedidos detallados y ademas tenemos un boton para dar de alta nuevos pedidos.
#
#    filters = get_filtros(request.GET, models.PedidoAlaboratorio)
#    mfilters = dict(filter(lambda v: v[0] in models.PedidoAlaboratorio.FILTROS, filters.items()))
#    pedidosAlab = models.PedidoAlaboratorio.objects.filter(**mfilters)
#    return render(request, "pedidos_A_laboratorio/listadoPedidoALaboratorio.html", {"pedidosAlab": pedidosAlab, "filtros": filters})
#
##=====================================================================================================================================
#
#def pedidoAlaboratorios_verRenglones(request, id):#Vista "a la que le pega" la url: r'^pedidoAlaboratorios/verRenglones/(?P<id>\d+)/$
#                                                  #por esta razon aparece el parametro id que es el identificador de un laboratorio.
#    pedidoALab = get_object_or_404(models.PedidoAlaboratorio, pk=id)#Se guarda en 'pedidoAlab' un pedido a laboratorio determinado
#                                                                    #accediendo a models con su identificador (ID de un laboratorio).
#
#    detalles=models.DetallePedidoAlaboratorio.objects.filter(pedido=pedidoALab.numero)#Se guarda en 'detalles' todos los (renglones) que
#                                                                                  #conforman a un pedido a laboratorio determinado
#                                                                                  #segun su id.
#    return render(request, "pedidos_A_laboratorio/VerRenglonesPedidoLab.html", {'nombreLab': pedidoALab.laboratorio.razonSocial, 'numeroPedido': pedidoALab.pk, 'fecha':pedidoALab.fecha, 'detalles': detalles})
#
#
#
##======================================================================================================================================
#
##================================INICIO DE LOGICA DE PROCESAMIENTO DE PEDIDOS DE FARMACIAS PENDIENTES==================================
#
#def verificarPedidosDeFarmacia(request, pkLaboratorio):
#    pendientesDeFarmacias = models.PedidoDeFarmacia.objects.filter( Q(estado = 'Pendiente')|Q(estado = 'Parcialmente Enviado') )
#
#    #Se ecorren todos los pedidos pendientes de las farmacias y vemos cada renglon(detalle) de estos pedidos para procesar cada uno de ellos.
#    #renglones = request.session.setdefault("renglones", [])
#    renglones = request.session["renglones"]=[]
#    for pendientes in pendientesDeFarmacias:
#        renglonesPedidoFarmacia = models.DetallePedidoDeFarmacia.objects.filter( Q(pedidoDeFarmacia=pendientes.pk) & Q( estaPedido=False ) & Q( medicamento__laboratorio=pkLaboratorio ))
#
#        for detPedFarm in renglonesPedidoFarmacia:
#            renglones.append({ "medicamento": detPedFarm.medicamento.pk, "nombre": detPedFarm.medicamento.nombreFantasia.nombreF,  "cantidad": detPedFarm.cantidadPendiente, "cantidadPendiente": detPedFarm.cantidadPendiente, "pk": detPedFarm.pk})
#            request.session.save()
#
#
##==============================================FIN LOGICA DE PROCESAMIENTO DE PEDIDOS PENDIENTES (FALTA )=======================================
#
#def pedidoAlaboratorios_agregarRenglones(request):
#
#    if "idLab" in request.session:
#        numero=request.session["idLab"]#Obtiene de la sesion el id de un laboratorio que se habia guardado previamente.
#
#    unLaboratorio = get_object_or_404(omodels.Laboratorio, pk=numero)#Obtiene la instancia de un laboratorio en base a numero (su ID).
#    nombreLab=unLaboratorio.razonSocial#Obtiene el nombre ('Razon Social') de un laboratorio de la instancia previa ('unLaboratorio').
#
#    nroPedido = get_next_nro_pedido_laboratorio(models.PedidoAlaboratorio, "numero")
#
#    hoy=datetime.datetime.now().strftime("%a, %d  de  %b del %Y")#En hoy se guarda la fecha actual (del sistema) con el formato
#                                                                 #seleccionado.
#
#    renglones = request.session.setdefault("renglones", [])
#    if request.method == "POST":
#
#        detallePedidoLab_form=forms.DetallePedidoLaboratorioFormFactory(unLaboratorio.pk)(request.POST)
#
#        if '_agregar' in request.POST :
#            if detallePedidoLab_form.is_valid():
#                detpedido = detallePedidoLab_form.save(commit=False)
#
#                renglones.append({ "medicamento": detpedido.medicamento.pk, "nombre": detpedido.medicamento.nombreFantasia.nombreF,  "cantidad": detpedido.cantidad, "cantidadPendiente": detpedido.cantidad, "pk":0})
#
#                request.session.save()
#                return render(request, "pedidos_A_laboratorio/AgregarRenglonesPedidoLab.html", {'id': numero, 'detalle': detallePedidoLab_form,  'renglones': renglones, 'nombreLab': nombreLab, 'nroPedido':nroPedido, 'hoy': hoy})
#        else:
#
#            pedidoALab=models.PedidoAlaboratorio(laboratorio=unLaboratorio)
#            pedidoALab.save()
#
#            for renglon in renglones:
#
#                medicamento=mmodels.Medicamento.objects.get(pk=renglon["medicamento"])
#                detallePed=models.DetallePedidoAlaboratorio(medicamento=medicamento, cantidad=renglon["cantidad"], pedido=pedidoALab, cantidadPendiente=renglon["cantidad"])
#
#                if renglon["pk"]>0:
#                    detallePedFarm=models.DetallePedidoDeFarmacia.objects.get(pk=renglon["pk"])
#                    detallePedFarm.estaPedido=True
#                    detallePedFarm.save()
#
#                    detallePed.detallePedidoFarmacia=detallePedFarm
#                    detallePed.save()
#
#            del request.session["renglones"]
#            del request.session["idLab"]
#
#            return redirect("/pedidoAlaboratorios/verRenglones/"+str(pedidoALab.pk))
#
#    else:
#
#        verificarPedidosDeFarmacia(request, unLaboratorio.pk)#para procesar los pedidos de farmacia
#        detallePedidoLab_form = forms.DetallePedidoLaboratorioFormFactory(unLaboratorio.pk)()
#
#        detallePedidoLab_form = forms.DetallePedidoLaboratorioFormFactory(unLaboratorio.pk)()
#        return render(request, "pedidos_A_laboratorio/AgregarRenglonesPedidoLab.html", {'id': numero, 'detalle': detallePedidoLab_form, 'renglones': renglones, 'nombreLab': nombreLab, 'nroPedido':nroPedido, 'hoy': hoy})
#

"""
#---AgregarLotes
def pedidoAlaboratorios_agregarLotes(request):

    if "idLab" in request.session:
        numero=request.session["idLab"]#Obtiene de la sesion el id de un laboratorio que se habia guardado previamente.

    unLaboratorio = get_object_or_404(omodels.Laboratorio, pk=numero)#Obtiene la instancia de un laboratorio en base a numero (su ID).
    nombreLab=unLaboratorio.razonSocial#Obtiene el nombre ('Razon Social') de un laboratorio de la instancia previa ('unLaboratorio').

    nroPedido= models.PedidoAlaboratorio.objects.count()+1 #El numero de pedido se obtiene contando todos las pedidos ya realizados
                                                           #(que estan en la base de datos) y sumandole 1 ya que sera un nuevo numero
                                                           #de pedido a laboratorio que se va a dar de alta.

    hoy=datetime.datetime.now().strftime("%a, %d  de  %b del %Y")#En hoy se guarda la fecha actual (del sistema) con el formato
                                                                 #seleccionado.

    renglones = request.session.setdefault("renglones", [])
    if request.method == "POST":

        detallePedidoLab_form=forms.DetallePedidoLaboratorioFormFactory(unLaboratorio.pk)(request.POST)

        if '_agregar' in request.POST :
            if detallePedidoLab_form.is_valid():
                detpedido = detallePedidoLab_form.save(commit=False)

                renglones.append({ "medicamento": detpedido.medicamento.pk, "nombre": detpedido.medicamento.nombreFantasia.nombreF,  "cantidad": detpedido.cantidad, "cantidadPendiente": detpedido.cantidad, "pk":0})

                request.session.save()
                return render(request, "pedidos_A_laboratorio/AgregarRenglonesPedidoLab.html", {'id': numero, 'detalle': detallePedidoLab_form,  'renglones': renglones, 'nombreLab': nombreLab, 'nroPedido':nroPedido, 'hoy': hoy})
        else:

            pedidoALab=models.PedidoAlaboratorio(laboratorio=unLaboratorio)
            pedidoALab.save()

            for renglon in renglones:

                medicamento=mmodels.Medicamento.objects.get(pk=renglon["medicamento"])
                detallePed=models.DetallePedidoAlaboratorio(medicamento=medicamento, cantidad=renglon["cantidad"], pedido=pedidoALab, cantidadPendiente=renglon["cantidad"])

                if renglon["pk"]>0:
                    detallePedFarm=models.DetallePedidoDeFarmacia.objects.get(pk=renglon["pk"])
                    detallePedFarm.estaPedido=True
                    detallePedFarm.save()
                    detallePed.detallePedidoFarmacia=detallePedFarm

                detallePed.save()
            del request.session["renglones"]
            del request.session["idLab"]

            return redirect("/pedidoAlaboratorios/verRenglones/"+str(pedidoALab.pk))

    else:

        verificarPedidosDeFarmacia(request, unLaboratorio.pk)#para procesar los pedidos de farmacia

        detallePedidoLab_form = forms.DetallePedidoLaboratorioFormFactory(unLaboratorio.pk)()
        return render(request, "pedidos_A_laboratorio/AgregarLotes.html", {'id': numero, 'detalle': detallePedidoLab_form, 'renglones': renglones, 'nombreLab': nombreLab, 'nroPedido':nroPedido, 'hoy': hoy})

#---fin agregar lotes

#========================================FIN PEDIDOS A LABORATORIOS==================================================================



#======================================================================================================================================

#=====================================================================================================================================

def pedidoAlaboratorios_RecepcionPedidoLab(request, id):#Vista "a la que le pega" la url: r'^pedidoAlaboratorios/verRenglones/(?P<id>\d+)/$
                                                  #por esta razon aparece el parametro id que es el identificador de un laboratorio.
    pedidoALab = get_object_or_404(models.PedidoAlaboratorio, pk=id)#Se guarda en 'pedidoAlab' un pedido a laboratorio determinado
                                                                    #accediendo a models con su identificador (ID de un laboratorio).
    detalles=models.DetallePedidoAlaboratorio.objects.filter(pedido=pedidoALab.pk)#Se guarda en 'detalles' todos los (renglones) que
                                                                                  #conforman a un pedido a laboratorio determinado
                                                                                  #segun su id.
    return render(request, "pedidos_A_laboratorio/RegistrarRecepcionPedido.html", {'nombreLab': pedidoALab.laboratorio.razonSocial, 'numeroPedido': pedidoALab.pk, 'fecha':pedidoALab.fecha, 'detalles': detalles})
#========================================FIN RECEPCION DE PEDIDO A LABORATORIO=======================================================

"""
#========================================INICIO RECEPCION DE PEDIDO A LABORATORIO====================================================

@login_required(login_url='login')
def recepcionPedidoAlaboratorio(request):
  mfilters = get_filtros(request.GET, models.PedidoAlaboratorio)
  pedidos = models.PedidoAlaboratorio.objects.filter(**mfilters)
  fecha = datetime.datetime.now()
  recibidos = pedidos.filter( Q(estado = 'Pendiente')|Q(estado = 'Parcialmente enviado') )
  return render(request, "recepcionPedidoALaboratorio/pedidos.html", {'recibidos': recibidos,'fecha':fecha, "filtros": request.GET})


def recepcionPedidoAlaboratorio_control(request, id_pedido):
    pedido = get_object_or_404(models.PedidoAlaboratorio, pk=id_pedido)
    detalles = models.DetallePedidoAlaboratorio.objects.filter(pedido=pedido.numero)
    return render(request, "recepcionPedidoALaboratorio/controlPedido.html", {'pedido': pedido, 'detalles': detalles})

def recepcionPedidoAlaboratorio_controlDetalle(request, id_pedido, id_detalle):
    pedido = get_object_or_404(models.PedidoAlaboratorio, pk = id_pedido)
    detalle = get_object_or_404(models.DetallePedidoAlaboratorio, pk = id_detalle)
    return render(request, "recepcionPedidoALaboratorio/controlDetalle.html", {'pedido': pedido, 'detalle': detalle})

class remitoPDF(PDFTemplateView):
    template_name = "remitopdf.html"

    def get_context_data(self, id_pedido):
        remito = models.Remito.objects.filter(pedidoFarmacia__pk=id_pedido).latest("id")
        detallesRemito = models.DetalleRemito.objects.filter(remito=remito)
        return super(remitoPDF, self).get_context_data(
            pagesize="A4",
            remito= remito,
            detallesRemito = detallesRemito
        )
