from django.shortcuts import render, redirect, get_object_or_404
from pedidos import forms, models
from django.contrib.auth.decorators import login_required
import datetime
# Create your views here.

def get_filtros(get, modelo):
    mfilter = {}
    for filtro in modelo.FILTROS:
        attr = filtro.split("__")[0]
        if attr in get and get[attr]:
            mfilter[filtro] = get[attr]
            mfilter[attr] = get[attr]
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

#PEDIDO DE FARMACIA#
@login_required(login_url='login')
def pedidoDeFarmacia(request):
    if request.method == "POST":
        form = forms.PedidoFarmaciaForm(request.POST)
        if form.is_valid():
            pedido = form.save()
            return redirect('detallesPedidoFarmacia', pedido.nroPedido)
    else:
        form = forms.PedidoFarmaciaForm()
    return render(request, "pedidoDeFarmacia.html",{"form": form })

@login_required(login_url='login')
def detallesPedidoFarmacia(request, id_pedido):
    detalles = models.DetallePedidoFarmacia.objects.filter(pedidoFarmacia=id_pedido)
    return render(request,"detallesPedidoFarmacia.html", {"detalles": detalles, "id_pedido": id_pedido})

@login_required(login_url='login')
def addDetallesPedidoFarmacia(request, id_pedido):
    if request.method == "POST":
        form = forms.DetallePedidoFarmaciaForm(request.POST)
        if form.is_valid():
            detalle = form.save(commit=False)
            pedido = get_object_or_404(models.PedidoFarmacia, pk=id_pedido)
            detalle.pedidoFarmacia = pedido
            detalle.save()
            if '_volver' in request.POST:
                return redirect('detallesPedidoFarmacia', id_pedido)
            else:
                return redirect('addDetallesPedidoFarmacia', id_pedido)
    else:
        form = forms.DetallePedidoFarmaciaForm()
    return render(request, "addDetallesPedidoFarmacia.html",{"form": form, "id_pedido": id_pedido})

@login_required(login_url='login')
def deleteDetallesPedidoFarmacia(request, id_pedido, id_detalle):
    detalle = get_object_or_404(models.DetallePedidoFarmacia, pedidoFarmacia= id_pedido, pk=id_detalle)
    detalle.delete()
    return redirect('detallesPedidoFarmacia', id_pedido)

#@login_required(login_url='login')
#def ListPedidoALaboratorio(request):
#  ListPedidoALaboratorio = models.PedidoAlaboratorio

 # return render(request, "listadoPedidoALaboratorio.html")



#===============================================PEDIDOS A LABORTORIO==================================================================

@login_required(login_url='login')
def PedidoLaboratorio_add(request):

    if request.method == "POST":
        pedidoALaboratorio_form = forms.PedidoLaboratorioForm(request.POST)
        if pedidoALaboratorio_form.is_valid():
            nro=pedidoALaboratorio_form.cleaned_data['numero']

            pedidoALaboratorio_form.save()



            if '_volver' in request.POST:
                return redirect("/pedidoAlaboratorios/verRenglones/"+str(nro))
            else:
                return redirect("/pedidoAlaboratorios/verRenglones/"+str(nro))
    else:
        pedidoALaboratorio_form = forms.PedidoLaboratorioForm()
    return render(request, 'pedidos_A_laboratorio/PedidoAlaboratorioAdd.html', {"pedidoALaboratorio_form": pedidoALaboratorio_form})


@login_required(login_url='login')
def ListPedidoALaboratorio(request):
    filters = get_filtros(request.GET, models.PedidoAlaboratorio)
    mfilters = dict(filter(lambda v: v[0] in models.PedidoAlaboratorio.FILTROS, filters.items()))
    pedidosAlab = models.PedidoAlaboratorio.objects.filter(**mfilters)
    return render(request, "pedidos_A_laboratorio/listadoPedidoALaboratorio.html", {"pedidosAlab": pedidosAlab, "filtros": filters})


def pedidoAlaboratorios_verRenglones(request, numero):
    pedidoALab = get_object_or_404(models.PedidoAlaboratorio, pk=numero)
    if request.method == "POST":
        form = forms.PedLaboratorioVerRenglonesForm(request.POST, instance=pedidoALab)
        if form.is_valid():
            form.save()
            return redirect('c')
    else:
        form = forms.PedLaboratorioVerRenglonesForm(instance=pedidoALab)
    return render(request, "pedidos_A_laboratorio/VerRenglonesPedidoLab.html", {'form': form, 'id': numero})

#========================================FIN PEDIDOS A LABORATORIOS==================================================================


