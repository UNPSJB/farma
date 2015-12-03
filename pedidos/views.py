

from django.db.models import Q # Herramienta que nos permite "darle de comer" expresiones con OR a los filter


from medicamentos import models as mmodels
from organizaciones import models as omodels

# Create your views here.
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
            utils.procesar_pedido(p)
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

#===============================================PEDIDOS A LABORATORIO==================================================================

@login_required(login_url='login')
def PedidoLaboratorio_add(request):#metodo que crea un nuevo pedido a laboratorio

    if request.method == "POST": #si el metodo request es por post
        pedidoALaboratorio_form = forms.PedidoLaboratorioForm(request.POST)#El formulario 'PedidoLaboratorioForm' con los datos actuales del POST
                                                                           #se guarda en pedidoALaboratorio_form

        if pedidoALaboratorio_form.is_valid():#si los datos en el formulario son validos

            pedido=pedidoALaboratorio_form.save(commit=False)#El pedidoALaboratorio_form se guarda en pedido pero no en la base.
            request.session["idLab"]=pedido.laboratorio.pk#Se obtiene el id que identifica al laboratorio y se mete en la sesion.

            if '_continuar' in request.POST:#Si el metodo POST trae el valor '_continuar' que pertenece al boton 'crear pedido' debe redirigir a el template 'AgregarRenglonesPedidoLab'
                return redirect("/pedidoAlaboratorios/agregarRenglones/")

    else: #si no si viene por GET
        pedidoALaboratorio_form = forms.PedidoLaboratorioForm()#cuando no viene por POST el formulario 'PedidoLaboratorioForm' se guarda en pedidoALaboratorio_form
        return render(request, 'pedidos_A_laboratorio/PedidoAlaboratorioAdd.html', {"pedidoALaboratorio_form": pedidoALaboratorio_form})#Renderiza el formulario en el template para poder elegir
                                                                                                                                        #un laboratorio al cual se desea realizar un pedido.

#======================================================================================================================================

@login_required(login_url='login')
def ListPedidoALaboratorio(request): #Vista "a la que le pega" la url: r'^ListPedidoALaboratorio/$' que luego renderiza la primer
                                     #pantalla que vemos al comenzar con el proceso de pedidos a laboratorios, en esta pantalla
                                     #se pueden ver todos los pedidos que se hicieron a laboratorio ,tenemos el acceso
                                     #para ver estos pedidos detallados y ademas tenemos un boton para dar de alta nuevos pedidos.

    filters = get_filtros(request.GET, models.PedidoAlaboratorio)
    mfilters = dict(filter(lambda v: v[0] in models.PedidoAlaboratorio.FILTROS, filters.items()))
    pedidosAlab = models.PedidoAlaboratorio.objects.filter(**mfilters)
    return render(request, "pedidos_A_laboratorio/listadoPedidoALaboratorio.html", {"pedidosAlab": pedidosAlab, "filtros": filters})

#=====================================================================================================================================

def pedidoAlaboratorios_verRenglones(request, id):#Vista "a la que le pega" la url: r'^pedidoAlaboratorios/verRenglones/(?P<id>\d+)/$
                                                  #por esta razon aparece el parametro id que es el identificador de un laboratorio.
    pedidoALab = get_object_or_404(models.PedidoAlaboratorio, pk=id)#Se guarda en 'pedidoAlab' un pedido a laboratorio determinado
                                                                    #accediendo a models con su identificador (ID de un laboratorio).
    detalles=models.DetallePedidoAlaboratorio.objects.filter(pedido=pedidoALab.pk)#Se guarda en 'detalles' todos los (renglones) que
                                                                                  #conforman a un pedido a laboratorio determinado
                                                                                  #segun su id.
    return render(request, "pedidos_A_laboratorio/VerRenglonesPedidoLab.html", {'nombreLab': pedidoALab.laboratorio.razonSocial, 'numeroPedido': pedidoALab.pk, 'fecha':pedidoALab.fecha, 'detalles': detalles})

#======================================================================================================================================

#=====================================================================================================================================

def pedidoAlaboratorios_RecepcionPedidoLab(request, id):#Vista "a la que le pega" la url: r'^pedidoAlaboratorios/verRenglones/(?P<id>\d+)/$
                                                  #por esta razon aparece el parametro id que es el identificador de un laboratorio.
    pedidoALab = get_object_or_404(models.PedidoAlaboratorio, pk=id)#Se guarda en 'pedidoAlab' un pedido a laboratorio determinado
                                                                    #accediendo a models con su identificador (ID de un laboratorio).
    detalles=models.DetallePedidoAlaboratorio.objects.filter(pedido=pedidoALab.pk)#Se guarda en 'detalles' todos los (renglones) que
                                                                                  #conforman a un pedido a laboratorio determinado
                                                                                  #segun su id.
    return render(request, "pedidos_A_laboratorio/VerRenglonesPedidoLab.html", {'nombreLab': pedidoALab.laboratorio.razonSocial, 'numeroPedido': pedidoALab.pk, 'fecha':pedidoALab.fecha, 'detalles': detalles})

#======================================================================================================================================

#================================INICIO DE LOGICA DE PROCESAMIENTO DE PEDIDOS DE FARMACIAS PENDIENTES==================================

def verificarPedidosDeFarmacia(request, pkLaboratorio): #***********************************************************************
    pkLab = pkLaboratorio
    #Se obtienen todos los pedidos de farmacias pendientes o parcialmente enviados.
    pendientesDeFarmacias = models.PedidoDeFarmacia.objects.filter( Q(estado = 'Pendiente')|Q(estado = 'Parcialmente enviado') )

    #Se ecorren todos los pedidos pendientes de las farmacias y vemos cada renglon(detalle) de estos pedidos para procesar cada uno de ellos.
    renglones = request.session.setdefault("renglones", [])

    for pendientes in pendientesDeFarmacias:
        renglonesPedidoFarmacia = models.DetallePedidoDeFarmacia.objects.filter( Q(pedidoDeFarmacia=pendientes.pk) & Q( estaPedido=False ) & Q( medicamento__laboratorio=pkLaboratorio ))
        print renglonesPedidoFarmacia
        for detPedFarm in renglonesPedidoFarmacia:

            renglones.append({ "medicamento": detPedFarm.medicamento.pk, "nombre": detPedFarm.medicamento.nombreFantasia.nombreF,  "cantidad": detPedFarm.cantidad, "cantidadPendiente": detPedFarm.cantidad, "pk": detPedFarm.pk})
            request.session.save()


#==============================================FIN LOGICA DE PROCESAMIENTO DE PEDIDOS PENDIENTES (FALTA )=======================================

def pedidoAlaboratorios_agregarRenglones(request):

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
        return render(request, "pedidos_A_laboratorio/AgregarRenglonesPedidoLab.html", {'id': numero, 'detalle': detallePedidoLab_form, 'renglones': renglones, 'nombreLab': nombreLab, 'nroPedido':nroPedido, 'hoy': hoy})

#========================================FIN PEDIDOS A LABORATORIOS==================================================================

#========================================INICIO RECEPCION DE PEDIDO A LABORATORIO====================================================

@login_required(login_url='login')
def recepcionPedidoDeLaboratorio(request):
  fecha = datetime.datetime.now()
  recibidos = models.PedidoAlaboratorio.objects.filter( Q(estado = 'Pendiente')|Q(estado = 'Parcialmente enviado') )

  return render(request, "pedidos_A_laboratorio/recepcionPedidoDeLaboratorio.html", {'recibidos': recibidos,'fecha':fecha})

#========================================FIN RECEPCION DE PEDIDO A LABORATORIO=======================================================