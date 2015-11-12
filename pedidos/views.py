from django.shortcuts import render, redirect, get_object_or_404
from pedidos import forms, models
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json
import datetime

# Create your views here.

def get_filtros(get, modelo):
    mfilter = {}
    for filtro in modelo.FILTROS:
        if filtro in get and get[filtro]:
            attr = filtro
            if hasattr(models, "FILTERMAPPER") and filtro in models.PedidoFarmacia.FILTERMAPPER:
                attr = models.FILTERMAPPER[filtro]
            mfilter[attr] = get[filtro]
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
        filters = get_filtros(request.GET, models.RemitoMedVencido)
        mfilters = dict(filter(lambda v: v[0] in models.RemitoMedVencido.FILTROS, filters.items()))
        remitos = models.RemitoMedVencido.objects.filter(**mfilters)
    return render(request, "devMedicamentoVencidos.html",
        {"remitos": remitos,
         "filtros": filters,
         "form": form})

# ****** PEDIDOS DE FARMACIA ******
@login_required(login_url='login')
def pedidosDeFarmacia(request):
    filters = get_filtros(request.GET, models.PedidoFarmacia)
    mfilters = dict(filter(lambda v: v[0] in models.PedidoFarmacia.FILTROS, filters.items()))
    pedidos = models.PedidoFarmacia.objects.filter(**mfilters)
    return render(request, "pedidoDeFarmacia/pedidos.html", {"pedidos": pedidos, "filtros": filters})

@login_required(login_url='login')
def pedidoF_add(request):
    if request.method == "POST":
        form = forms.PedidoFarmaciaForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.estado = 'Enviado'
            pedido.save()
            return redirect('detalles_pedidoF', pedido.nroPedido)
    else:
        form = forms.PedidoFarmaciaForm()
    return render(request, "pedidoDeFarmacia/pedidoAdd.html", {"form": form})


@login_required(login_url='login')
def detalles_pedidoF(request, id_pedido):
    pedido = get_object_or_404(models.PedidoFarmacia, pk=id_pedido)
    detalles = models.DetallePedidoFarmacia.objects.filter(pedidoFarmacia=id_pedido)
    return render(request, "pedidoDeFarmacia/presentacionPedido.html", {"pedido": pedido,
                                                                 "detalles": detalles,
                                                                 "id_pedido": id_pedido})


@login_required(login_url='login')
def addDetalle_pedidoF(request, id_pedido):
    if request.method == "POST":
        form = forms.DetallePedidoFarmaciaForm(request.POST)
        if form.is_valid():
            detalle = form.save(commit=False)
            pedido = get_object_or_404(models.PedidoFarmacia, pk=id_pedido)
            detalle.pedidoFarmacia = pedido
            detalle.save()
            if '_volver' in request.POST:
                return redirect('detalles_pedidoF', id_pedido)
            else:
                return redirect('addDetalle_pedidoF', id_pedido)
    else:
        form = forms.DetallePedidoFarmaciaForm()
    return render(request, "pedidoDeFarmacia/detallePedidoAdd.html", {"form": form, "id_pedido": id_pedido})

@login_required(login_url='login')
def updateDetalle_pedidoF(request, id_pedido, id_detalle):
    detalle = get_object_or_404(models.DetallePedidoFarmacia, pk=id_detalle)
    if request.method == "POST":
        form = forms.DetallePedidoFarmaciaFormUpdate(request.POST, instance=detalle)
        if form.is_valid():
            form.save()
            return redirect('detalles_pedidoF', id_pedido)
    else:
        form = forms.DetallePedidoFarmaciaFormUpdate(instance=detalle)
    return render(request, "pedidoDeFarmacia/detallePedidoUpdate.html", {"form": form,
                                                                         "id_pedido": id_pedido,
                                                                         "id_detalle": id_detalle})

@login_required(login_url='login')
def deleteDetalle_pedidoF(request, id_pedido, id_detalle):
    detalle = get_object_or_404(models.DetallePedidoFarmacia, pk=id_detalle)
    detalle.delete();
    return redirect('detalles_pedidoF', id_pedido);

@login_required(login_url='login')
def get_detalles_pedido_farmacia_ajax(request):
    if request.is_ajax() and request.method == "GET":
        id_pedido = request.GET.get('id')
        detalles_pedido = models.DetallePedidoFarmacia.objects.filter(pedidoFarmacia=id_pedido)
        respuesta = []
        for detalle in detalles_pedido:
            detalle_json = {}
            detalle_json['medicamento'] = "%s - %s %s %s" % (detalle.medicamento.nombreFantasia.nombreF,
                                                             detalle.medicamento.presentacion.descripcion,
                                                             detalle.medicamento.presentacion.cantidad,
                                                             detalle.medicamento.presentacion.unidadMedida)
            detalle_json['cantidad'] = detalle.cantidad
            respuesta.append(detalle_json)
        return HttpResponse(json.dumps(respuesta), "application/json")

@login_required(login_url='login')
def despachar_pedidoF(request, id_pedido):
    if request.method == "POST":
        seleccionados = request.POST.getlist('seleccionado')
        if len(seleccionados)> 0:
            pedido = get_object_or_404(models.PedidoFarmacia, pk=id_pedido)
            remito = models.Remito()
            remito.pedidoFarmacia = pedido
            remito.fecha = datetime.datetime.now()
            remito.save()
            for item in seleccionados:
                detallePedido = models.DetallePedidoFarmacia.objects.get(pk=item)
                detalleRemito = models.DetalleRemito()
                detalleRemito.detallePedidoFarmacia = detallePedido
                detalleRemito.cantidad = detallePedido.cantidad
                detalleRemito.remito = remito
                detalleRemito.save()

    detalles = models.DetallePedidoFarmacia.objects.all()
    return render(request, "pedidoDeFarmacia/despacharPedido.html", {"detalles": detalles,
                                                                     "id_pedido": id_pedido})
