from django.shortcuts import render, redirect
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
def farmacias(request):
    farmacias = None
    filters = None
    if request.method == "POST":
        form = forms.FarmaciaForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return redirect('farmacias')
    else:
        form = forms.FarmaciaForm()
        filters = get_filtros(request.GET, models.Farmacia)
        mfilters = dict(filter(lambda v: v[0] in models.Farmacia.FILTROS, filters.items()))
        farmacias = models.Farmacia.objects.filter(**mfilters)
    return render(request, "farmacias.html",
        {"farmacias": farmacias,
         "filtros": filters,
         "form": form})

@login_required(login_url='login')
def clinicas(request):
    clinicas = None
    filters = None
    if request.method == "POST":
        form = forms.ClinicaForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return redirect('clinicas')
    else:
        form = forms.ClinicaForm()
        filters = get_filtros(request.GET, models.Clinica)
        mfilters = dict(filter(lambda v: v[0] in models.Clinica.FILTROS, filters.items()))
        clinicas = models.Clinica.objects.filter(**mfilters)
    return render(request, "clinicas.html",
        {"clinicas": clinicas,
         "filtros": filters,
         "form": form})

@login_required(login_url='login')
def laboratorios(request):
    laboratorios = None
    filters = None
    if request.method == "POST":

        form = forms.LaboratorioForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return redirect('laboratorios')
        else:
            print("holass")
    else:
        form = forms.LaboratorioForm()
        filters = get_filtros(request.GET, models.Laboratorio)
        mfilters = dict(filter(lambda v: v[0] in models.Laboratorio.FILTROS, filters.items()))
        laboratorios = models.Laboratorio.objects.filter(**mfilters)
    return render(request, "laboratorios.html",
        {"laboratorios": laboratorios,
         "filtros": filters,
         "form": form})