from django.shortcuts import render, redirect
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
  fecha = datetime.datetime.now()
  return render(request, "pedidoDeFarmacia.html",{'fecha_pedido': fecha})
