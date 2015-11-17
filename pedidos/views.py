from django.shortcuts import render, redirect, get_object_or_404, RequestContext
from jsonview.decorators import json_view
from pedidos import forms, models, utils
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from crispy_forms.utils import render_crispy_form
from django.core import serializers
from medicamentos.models import Medicamento
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
def ver_pedidoF(request, id_pedido):
    pedido = get_object_or_404(models.PedidoFarmacia,pk=id_pedido)
    detalles = models.DetallePedidoFarmacia.objects.filter(pedidoFarmacia=pedido)
    return render(request, "pedidoDeFarmacia/ver-pedido.html",{"pedido": pedido, "detalles": detalles})


@login_required(login_url='login')
def deleteDetalle_pedidoF(request, id_pedido, id_detalle):
    detalle = get_object_or_404(models.DetallePedidoFarmacia, pk=id_detalle)
    detalle.delete();
    return redirect('detalles_pedidoF', id_pedido)


# ********************************** CRISPY FORMS **********************************
@ensure_csrf_cookie
@json_view
@login_required(login_url='login')
def add_detalle_pedido_farmacia(request):
    success = False
    new_form = False
    detalle_json = None
    if request.method == 'POST':
        form = forms.DetallePedidoFarmaciaForm(request.POST)
        if form.is_valid():
            detalle = form.save(commit=False)
            id_pedido = int(request.POST.get('id_pedido'))
            detalle.pedidoFarmacia = get_object_or_404(models.PedidoFarmacia, pk=id_pedido)
            detalle_json = serializers.serialize('python', [detalle])
            success = True
            new_form = True
    else:
        new_form = True

    if new_form:
        form = forms.DetallePedidoFarmaciaForm()

    request_context = RequestContext(request)
    form_html = render_crispy_form(form, context=request_context)
    return {'new_form': new_form, 'success': success, 'form_html': form_html, 'detalle': detalle_json}

@ensure_csrf_cookie
@json_view
@login_required(login_url='login')
def update_detalle_pedido_farmacia(request, id_detalle):
    success = False

    if request.method == 'POST':
        detalle = request.POST.get('detalle')
        list_deserializer = serializers.deserialize('json', detalle)
        for obj in list_deserializer:
            detalle = models.DetallePedidoFarmacia(pedidoFarmacia=obj.object.pedidoFarmacia, medicamento=obj.object.medicamento, cantidad=obj.object.cantidad)
        form = forms.UpdateDetallePedidoFarmaciaForm(request.POST, instance=detalle)

        if form.is_valid():
            detalle = form.save(commit=False)
            detalle_json = serializers.serialize('python', [detalle])
            success = True
            return {'success': success, 'detalle': detalle_json}
    else:
        detalle = request.GET.get('detalle')
        list_deserializer = serializers.deserialize('json', detalle)

        for obj in list_deserializer:
            detalle = models.DetallePedidoFarmacia(pedidoFarmacia=obj.object.pedidoFarmacia, medicamento=obj.object.medicamento, cantidad=obj.object.cantidad)
        form = forms.UpdateDetallePedidoFarmaciaForm(instance=detalle)

    request_context = RequestContext(request)
    form_html = render_crispy_form(form, context=request_context)
    return {'success': success, 'form_html': form_html}


@json_view
@login_required(login_url='login')
def registrar_pedido_farmacia(request):
    if request.method == 'POST':
        id_pedido = request.POST.get('id_pedido')

        detalles_pedido = models.DetallePedidoFarmacia.objects.filter(pedidoFarmacia__nroPedido=id_pedido)
        #Si el pedido no tiene detalles en la db, significa que todavia no registro el pedido completo
        if not detalles_pedido:
            list_deserializer = serializers.deserialize('json', request.POST.get('detalles'))
            for obj in list_deserializer:
                detalle = models.DetallePedidoFarmacia(pedidoFarmacia=obj.object.pedidoFarmacia, medicamento=obj.object.medicamento, cantidad=obj.object.cantidad)
                utils.procesar_detalle(detalle)
                detalle.save()
            utils.setearEstado(id_pedido)
            return {'success': True}
        else:
            #Si el pedido tiene detalles en la db, significa que ya se registro anteriormente
            return {'success': False}