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

def monodrogas(request):
    monodrogas = None
    filters = None
    if request.method == "POST":
        form = forms.MonodrogaForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return redirect('monodrogas')
    else:
        form = forms.MonodrogaForm()
        filters = get_filtros(request.GET, models.Monodroga)
        mfilters = dict(filter(lambda v: v[0] in models.Monodroga.FILTROS, filters.items()))
        monodrogas = models.Monodroga.objects.filter(**mfilters)
    return render(request, "medicamentos/monodrogas.html",
        {"monodrogas": monodrogas,
         "filtros": filters,
         "form": form})

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
    nombresFantasia = None
    filters = None
    if request.method == "POST":
        form = forms.NombreFantasiaForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return redirect('nombresFantasia')
    else:
        form = forms.NombreFantasiaForm()
        filters = get_filtros(request.GET, models.NombreFantasia)
        mfilters = dict(filter(lambda v: v[0] in models.NombreFantasia.FILTROS, filters.items()))
        nombresFantasia = models.NombreFantasia.objects.filter(**mfilters)
    return render(request, "NombreFantasia.html",
        {"nombresFantasia": nombresFantasia,
         "filtros": filters,
         "form": form})


@login_required(login_url='login')
def presentacion(request):
    presentaciones = None
    filters = None
    if request.method == "POST":
        form = forms.PresentacionForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return redirect('presentacion')
    else:
        form = forms.PresentacionForm()
        filters = get_filtros(request.GET, models.Presentacion)
        mfilters = dict(filter(lambda v: v[0] in models.Presentacion.FILTROS, filters.items()))
        presentaciones = models.Presentacion.objects.filter(**mfilters)
    return render(request, "Presentacion.html",
        {"presentaciones": presentaciones,
         "filtros": filters,
         "form": form})