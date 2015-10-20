from django.shortcuts import render, redirect, get_object_or_404
from . import models
from . import forms
from django.contrib.auth import authenticate, login, logout
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

@login_required(login_url='login')
def monodrogas(request):
    filters = get_filtros(request.GET, models.Monodroga)
    mfilters = dict(filter(lambda v: v[0] in models.Monodroga.FILTROS, filters.items()))
    monodrogas = models.Monodroga.objects.filter(**mfilters)
    return render(request, "Monodrogas.html", {"monodrogas": monodrogas, "filtros": filters})

@login_required(login_url='login')
def monodroga_add(request):
    if request.method == "POST":
        form = forms.MonodrogaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('monodroga_add')
    else:
        form = forms.MonodrogaForm()
    return render(request, "MonodrogasAdd.html", {"form": form})

@login_required(login_url='login')
def monodroga_update(request, id_monodroga):
    monodroga = get_object_or_404(models.Monodroga, pk=id_monodroga)
    if request.method == "POST":
        form = forms.MonodrogaForm(request.POST, instance=monodroga)
        if form.is_valid():
            form.save()
            return redirect('monodrogas')
    else:
        form = forms.MonodrogaForm(instance=monodroga)
    return render(request, "MonodrogasUpdate.html", {'form': form, 'id': id_monodroga})

@login_required(login_url='login')
def monodroga_delete(request, id_monodroga):
    monodroga = models.Monodroga.objects.get(pk=id_monodroga)
    monodroga.delete()
    return redirect('monodrogas')



@login_required(login_url='login')
def altaMedicamento(request):
    dosis_formset = forms.DosisFormSet()
    medicamento_form = forms.MedicamentoForm()
    if request.method == 'POST':
        medicamento_form = forms.MedicamentoForm(request.POST)
        dosis_formset = forms.DosisFormSet(request.POST)
        if medicamento_form.is_valid() and dosis_formset.is_valid():
            medicamento = medicamento_form.save()
            for dosis_form in dosis_formset:
                dosis = dosis_form.save(commit=False)
                dosis.medicamento = medicamento
                dosis.save()
            redirect("altaMedicamento")
    return render(request, "altaMedicamento.html", {
        "medicamento_form": medicamento_form,
        "dosis_formset": dosis_formset,
    })

@login_required(login_url='login')
def nombresFantasia(request):
    filters = get_filtros(request.GET, models.NombreFantasia)
    mfilters = dict(filter(lambda v: v[0] in models.NombreFantasia.FILTROS, filters.items()))
    nombresFantasias = models.NombreFantasia.objects.filter(**mfilters)
    return render(request, "NombreFantasia.html",{"nombresFantasias": nombresFantasias, "filtros": filters})

@login_required(login_url='login')
def nombresFantasia_add(request):
    if request.method == "POST":
        form = forms.NombreFantasiaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('nombresFantasia_add')
    else:
        form = forms.NombreFantasiaForm()
    return render(request, "NombreFantasiaAdd.html", {"form": form})

@login_required(login_url='login')
def nombresFantasia_update(request, id_nombreFantasia):
    nombresFantasias = get_object_or_404(models.NombreFantasia, pk=id_nombreFantasia)
    if request.method == "POST":
        form = forms.NombreFantasiaForm(request.POST, instance=nombresFantasias)
        if form.is_valid():
            form.save()
            return redirect('nombresFantasia')
    else:
        form = forms.NombreFantasiaForm(instance=nombresFantasias)
    return render(request, "NombreFantasiaUpdate.html", {'form': form, 'id': id_nombreFantasia})

@login_required(login_url='login')
def nombresFantasia_delete(request, id_nombreFantasia):
    nombreFantasia = models.NombreFantasia.objects.get(pk=id_nombreFantasia)
    nombreFantasia.delete()
    return redirect('nombresFantasia')



@login_required(login_url='login')
def presentacion(request):
    filters = get_filtros(request.GET, models.Presentacion)
    mfilters = dict(filter(lambda v: v[0] in models.Presentacion.FILTROS, filters.items()))
    presentaciones = models.Presentacion.objects.filter(**mfilters)
    return render(request, "Presentacion.html",{"presentaciones": presentaciones, "filtros": filters})



@login_required(login_url='login')
def presentacion_add(request):
    if request.method == "POST":
        form = forms.PresentacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('presentacion_add')
    else:
        form = forms.PresentacionForm()
    return render(request, "PresentacionAdd.html", {"form": form})

@login_required(login_url='login')
def presentacion_update(request, id_presentacion):
    presentacion = get_object_or_404(models.Presentacion, pk=id_presentacion)
    if request.method == "POST":
        form = forms.PresentacionForm(request.POST, instance=presentacion)
        if form.is_valid():
            form.save()
            return redirect('presentacion')
    else:
        form = forms.PresentacionForm(instance=presentacion)
    return render(request, "PresentacionUpdate.html", {'form': form, 'id': id_presentacion})

@login_required(login_url='login')
def presentacion_delete(request, id_presentacion):
    clinica = models.Presentacion.objects.get(pk=id_presentacion)
    clinica.delete()
    return redirect('presentacion')
