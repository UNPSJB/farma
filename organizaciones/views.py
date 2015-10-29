from django.shortcuts import render, redirect, get_object_or_404
from organizaciones import models, forms
from django.contrib.auth.decorators import login_required

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
    if request.method == "POST":
        form = forms.FarmaciaForm(request.POST)
        if form.is_valid():
            form.save()
            if '_volver' in request.POST:
                return redirect('farmacias')
            else:
                return redirect('farmacia_add')
    else:
        form = forms.FarmaciaForm()
    return render(request, "farmaciaAdd.html", {"form": form})
    
@login_required(login_url='login')
def farmacia_update(request, id_farmacia):
    farmacia = get_object_or_404(models.Farmacia, pk=id_farmacia)
    if request.method == "POST":
        form = forms.FarmaciaForm(request.POST, instance=farmacia)
        if form.is_valid():
            form.save()
            return redirect('farmacias')
    else:
        form = forms.FarmaciaForm(instance=farmacia)
    return render(request, "farmaciaUpdate.html", {'form': form, 'id': id_farmacia})

@login_required(login_url='login')
def farmacia_delete(request, id_farmacia):
    farmacia = get_object_or_404(models.Farmacia, pk=id_farmacia)
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
    if request.method == "POST":
        form = forms.ClinicaForm(request.POST)
        if form.is_valid():
            form.save()
            if '_volver' in request.POST:
                return redirect('clinicas')
            else:
                return redirect('clinica_add')
    else:
        form = forms.ClinicaForm()
    return render(request, "clinicaAdd.html", {"form": form})

@login_required(login_url='login')
def clinica_update(request, id_clinica):
    clinica = get_object_or_404(models.Clinica, pk=id_clinica)
    if request.method == "POST":
        form = forms.ClinicaForm(request.POST, instance=clinica)
        if form.is_valid():
            form.save()
            return redirect('clinicas')
    else:
        form = forms.ClinicaForm(instance=clinica)
    return render(request, "clinicaUpdate.html", {'form': form, 'id': id_clinica})

@login_required(login_url='login')
def clinica_delete(request, id_clinica):
    clinica = models.Clinica.objects.get(pk=id_clinica)
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
    if request.method == "POST":
        form = forms.LaboratorioForm(request.POST)
        if form.is_valid():
            form.save()
            if '_volver' in request.POST:
                return redirect('laboratorios')
            else:
                return redirect('laboratorio_add')
    else:
        form = forms.LaboratorioForm()
    return render(request, "laboratorioAdd.html", {"form": form})

@login_required(login_url='login')
def laboratorio_update(request, id_laboratorio):
    laboratorio = get_object_or_404(models.Laboratorio, pk=id_laboratorio)
    if request.method == "POST":
        form = forms.LaboratorioForm(request.POST, instance=laboratorio)
        if form.is_valid():
            form.save()
            return redirect('laboratorios')
    else:
        form = forms.LaboratorioForm(instance=laboratorio)
    return render(request, "laboratorioUpdate.html", {'form': form, 'id': id_laboratorio})

@login_required(login_url='login')
def laboratorio_delete(request, id_laboratorio):
    laboratorio = models.Laboratorio.objects.get(pk=id_laboratorio)
    laboratorio.delete()
    return redirect('laboratorios')