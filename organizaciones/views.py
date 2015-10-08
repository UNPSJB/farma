from django.shortcuts import render, redirect
from . import models
from . import forms
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
def farmacias(request):
    filters = get_filtros(request.GET, models.Farmacia)
    mfilters = dict(filter(lambda v: v[0] in models.Farmacia.FILTROS, filters.items()))
    farmacias = models.Farmacia.objects.filter(**mfilters)
    return render(request, "farmacias.html",
         {"farmacias": farmacias,
         "filtros": filters})

@login_required(login_url='login')
def farmacia_add(request):
    if request.method == "POST":
        form = forms.FarmaciaForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return redirect('farmacias')
    else:
        form = forms.FarmaciaForm()
    return render(request, "farmacias.html",
        {"form": form})

@login_required(login_url='login')
def farmacia_delete(request, id):
    farmacia = models.Farmacia.objects.get(pk = id)
    farmacia.delete()
    return redirect('farmacias')

@login_required(login_url='login')
def clinicas(request):
    filters = get_filtros(request.GET, models.Clinica)
    mfilters = dict(filter(lambda v: v[0] in models.Clinica.FILTROS, filters.items()))
    clinicas = models.Clinica.objects.filter(**mfilters)
    return render(request, "clinicas.html",
         {"clinicas": clinicas,
         "filtros": filters})

@login_required(login_url='login')
def clinica_add(request):
    if request.method == "POST":
        form = forms.ClinicaForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return redirect('clinicas')
    else:
        form = forms.ClinicaForm()
    return render(request, "clinicas.html",
        {"form": form})

@login_required(login_url='login')
def clinica_delete(request, id):
    clinica = models.Clinica.objects.get(pk = id)
    clinica.delete()
    return redirect('clinicas')

@login_required(login_url='login')
def laboratorios(request):
    filters = get_filtros(request.GET, models.Laboratorio)
    mfilters = dict(filter(lambda v: v[0] in models.Laboratorio.FILTROS, filters.items()))
    laboratorios = models.Laboratorio.objects.filter(**mfilters)
    return render(request, "laboratorios.html",
         {"laboratorios": laboratorios,
         "filtros": filters})

@login_required(login_url='login')
def laboratorio_add(request):
    if request.method == "POST":
        form = forms.LaboratorioForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return redirect('laboratorios')
    else:
        form = forms.LaboratorioForm()
    return render(request, "laboratorios.html",
        {"form": form})

@login_required(login_url='login')
def laboratorio_delete(request, id):
    laboratorio = models.Laboratorio.objects.get(pk = id)
    laboratorio.delete()
    return redirect('laboratorios')