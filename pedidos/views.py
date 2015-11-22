from django.shortcuts import render, redirect, get_object_or_404, RequestContext
from jsonview.decorators import json_view
from pedidos import forms, models, utils
from organizaciones.models import Farmacia
from django.contrib.auth.decorators import login_required
from crispy_forms.utils import render_crispy_form
from datetime import datetime
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

def remitos(request):
    remitos = None
    filters = None
    if request.method == "POST":
        form = forms.RemitoForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return redirect('remitos')
    else:
        form = forms.RemitoForm()
        filters = get_filtros(request.GET, models.RemitoMedicamentosVencido)
        mfilters = dict(filter(lambda v: v[0] in models.RemitoMedicamentosVencido.FILTROS, filters.items()))
        remitos = models.RemitoMedicamentosVencido.objects.filter(**mfilters)
    return render(request, "devMedicamentoVencidos.html",
        {"remitos": remitos,
         "filtros": filters,
         "form": form})

# ****** PEDIDOS DE FARMACIA ******
@login_required(login_url='login')
def pedidosDeFarmacia(request):
    mfilters = get_filtros(request.GET, models.PedidoDeFarmacia)
    pedidos = models.PedidoDeFarmacia.objects.filter(**mfilters)
    return render(request, "pedidoDeFarmacia/pedidos.html", {"pedidos": pedidos, "filtros": request.GET})

@login_required(login_url='login')
def pedidoF_add(request):
    if 'pedidoFarmacia' in request.session:
        del request.session['pedidoFarmacia']

    if 'detalles' in request.session:
        del request.session['detalles']

    if request.method == "POST":
        form = forms.PedidoFarmaciaForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.estado = 'Enviado'
            ultPedido = models.PedidoDeFarmacia.objects.latest("nroPedido")
            request.session['pedidoFarmacia'] = {'nroPedido': ultPedido.nroPedido+1, 'farmacia':{'id': pedido.farmacia.id, 'razonSocial': pedido.farmacia.razonSocial},
                                                 'fecha': pedido.fecha.strftime('%d/%m/%Y')}
            return redirect('detalles_pedidoF')
    else:
           form = forms.PedidoFarmaciaForm()
    return render(request, "pedidoDeFarmacia/pedidoAdd.html", {"form": form})


@login_required(login_url='login')
def detalles_pedidoF(request):
    #del request.session['detalles']
    detalles = request.session.setdefault("detalles", [])
    pedido = request.session['pedidoFarmacia']
    return render(request, "pedidoDeFarmacia/presentacionPedido.html", {'pedido': pedido, 'detalles': detalles})


@login_required(login_url='login')
def ver_pedidoF(request, id_pedido):
    pedido = get_object_or_404(models.PedidoDeFarmacia,pk=id_pedido)
    detalles = models.DetallePedidDeFarmacia.objects.filter(pedidoFarmacia=pedido)
    return render(request, "pedidoDeFarmacia/ver-pedido.html",{"pedido": pedido, "detalles": detalles})


@login_required(login_url='login')
def deleteDetalle_pedidoF(request, id_pedido, id_detalle):
    detalle = get_object_or_404(models.DetallePedidDeFarmacia, pk=id_detalle)
    detalle.delete()
    return redirect('detalles_pedidoF', id_pedido)


# ********************************** CRISPY FORMS **********************************
@json_view
@login_required(login_url='login')
def add_detalle_pedido_farmacia(request):
    success = True
    form = forms.DetallePedidoFarmaciaForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            det = form.save(commit=False)
            detalles = request.session['detalles']
            for detalle in detalles:
                if detalle['medicamento']['id'] == det.medicamento.id: #no puede haber dos detalles con el mismo medicamento
                    success = False
                    break
            if success:
                detalles.append({'renglon': len(detalles) + 1,
                             'medicamento': {"id": det.medicamento.id,
                                             "descripcion": det.medicamento.nombreFantasia.nombreF + " " +
                                                            det.medicamento.presentacion.descripcion + " " +
                                                            str(det.medicamento.presentacion.cantidad) + " " +
                                                            det.medicamento.presentacion.unidadMedida
                                             },
                             'cantidad': det.cantidad})
                request.session['detalles'] = detalles
                form = forms.DetallePedidoFarmaciaForm() #Nuevo form para seguir dando de alta
                form_html = render_crispy_form(form, context=RequestContext(request))
                return {'success': success, 'form_html': form_html, 'detalles': detalles}
    form_html = render_crispy_form(form, context=RequestContext(request))
    return {'success': success, 'form_html': form_html}


@json_view
@login_required(login_url='login')
def update_detalle_pedido_farmacia(request, id_detalle):
    detalles = request.session['detalles']
    detalle = models.DetallePedidDeFarmacia(cantidad=detalles[int(id_detalle) - 1]['cantidad'])
    if request.method == "POST":
        form = forms.UpdateDetallePedidoFarmaciaForm(request.POST, instance=detalle)
        if form.is_valid():
            det = form.save(commit=False)
            detalles[int(id_detalle) - 1]['cantidad'] = det.cantidad
            request.session['detalles'] = detalles
            return {'success': True, 'detalles': detalles}
        else:
            form_html = render_crispy_form(form, context=RequestContext(request))
            return {'success': False, 'form_html': form_html}
    else:
        form = forms.UpdateDetallePedidoFarmaciaForm(instance=detalle)
    form_html = render_crispy_form(form, context=RequestContext(request))
    return {'form_html': form_html}

@json_view
@login_required(login_url='login')
def delete_detalle_pedido_farmacia(request, id_detalle):
    detalles = request.session['detalles']
    del detalles[int(id_detalle) - 1]
    for i in range(0, len(detalles)):
        detalles[i]['renglon'] = i + 1
    request.session['detalles'] = detalles
    return {'detalles': detalles}

#https://github.com/incuna/django-wkhtmltopdf !!!!!!!!!!!!!!!

@json_view
@login_required(login_url='login')
def registrar_pedido_farmacia(request):
    pedido = request.session['pedidoFarmacia']
    detalles = request.session['detalles']

    if detalles:
        farmacia = get_object_or_404(Farmacia, pk=pedido['farmacia']['id'])
        fecha = datetime.datetime.strptime(pedido['fecha'], '%d/%m/%Y').date()

        if not(models.PedidoDeFarmacia.objects.filter(pk=pedido["nroPedido"]).exists()):
            p = models.PedidoDeFarmacia(farmacia=farmacia, fecha=fecha, estado='Enviado')
            p.save()

            for detalle in detalles:
                medicamento = get_object_or_404(Medicamento, pk=detalle['medicamento']['id'])
                d = models.DetallePedidDeFarmacia(pedidoFarmacia=p, medicamento=medicamento, cantidad=detalle['cantidad'])
                d.save()

            #FUNCION

            return {'success': True}
        else:
            return {'success': False, 'mensaje-error': "El pedido ya Existe!"}
    else:
        return {'success': False, 'mensaje-error': "No se puede registrar un pedido sin detalles"}
