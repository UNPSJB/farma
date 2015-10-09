from django.shortcuts import render, redirect, get_object_or_404
from organizaciones import models, forms
from django.contrib.auth.decorators import login_required
# Create your views here.

def get_filtros(get, modelo):
    mfilter = {}
    for filtro in modelo.FILTROS:
        attr = filtro.split("__")[0]
        if attr in get and get[attr]:
            mfilter[filtro] = get[attr]
            mfilter[attr] = get[attr]
    return mfilter

# ****** FARMACIAS ******

@login_required(login_url='login')
def farmacias(request):
    filters = get_filtros(request.GET, models.Farmacia)
    mfilters = dict(filter(lambda v: v[0] in models.Farmacia.FILTROS, filters.items()))
    farmacias = models.Farmacia.objects.filter(**mfilters)
    return render(request, "farmacias.html", {"farmacias": farmacias, "filtros": filters})

@login_required(login_url='login')
def farmacia_add(request):
    form = forms.FarmaciaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('farmacias')
    return render(request, "farmacias.html", {"form": form})

@login_required(login_url='login')
def farmacia_modify(request, pk):
    farmacia = get_object_or_404(models.Farmacia, pk=pk)
    form = forms.FarmaciaForm(request.POST or None, instance=farmacia)
    if form.is_valid():
        form.save()
        return redirect('farmacias')
    return render(request, "farmacias.html", {'form': form})

@login_required(login_url='login')
def farmacia_delete(request, pk):
    farmacia = get_object_or_404(models.Farmacia, pk=pk)
    farmacia.delete()
    return redirect('farmacias')

# ****** CLINICAS ******

@login_required(login_url='login')
def clinicas(request):
    filters = get_filtros(request.GET, models.Clinica)
    mfilters = dict(filter(lambda v: v[0] in models.Clinica.FILTROS, filters.items()))
    clinicas = models.Clinica.objects.filter(**mfilters)
    return render(request, "clinicas.html",{"clinicas": clinicas, "filtros": filters})

@login_required(login_url='login')
def clinica_add(request):
    form = forms.ClinicaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('clinicas')
    return render(request, "clinicas.html", {"form": form})

@login_required(login_url='login')
def clinica_modify(request, pk):
    clinica = get_object_or_404(models.Clinica, pk=pk)
    form = forms.ClinicaForm(request.POST or None, instance=clinica)
    if form.is_valid():
        form.save()
        return redirect('clinicas')
    return render(request, "clinicas.html", {'form': form})

@login_required(login_url='login')
def clinica_delete(request, pk):
    clinica = models.Clinica.objects.get(pk=pk)
    clinica.delete()
    return redirect('clinicas')


# ******* LABORATORIOS ******

@login_required(login_url='login')
def laboratorios(request):
    filters = get_filtros(request.GET, models.Laboratorio)
    mfilters = dict(filter(lambda v: v[0] in models.Laboratorio.FILTROS, filters.items()))
    laboratorios = models.Laboratorio.objects.filter(**mfilters)
    return render(request, "laboratorios.html",{"laboratorios": laboratorios, "filtros": filters})

@login_required(login_url='login')
def laboratorio_add(request):
    form = forms.LaboratorioForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('laboratorios')
    return render(request, "laboratorios.html", {"form": form})

@login_required(login_url='login')
def laboratorio_modify(request, pk):
    laboratorio = get_object_or_404(models.Laboratorio, pk=pk)
    form = forms.LaboratorioForm(request.POST or None, instance=laboratorio)
    if form.is_valid():
        form.save()
        return redirect('laboratorios')
    return render(request, "laboratorios.html", {'form': form})

@login_required(login_url='login')
def laboratorio_delete(request, pk):
    laboratorio = models.Laboratorio.objects.get(pk=pk)
    laboratorio.delete()
    return redirect('laboratorios')