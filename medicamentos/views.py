from django.shortcuts import render, redirect, get_object_or_404
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
def monodrogas(request):
    filters = get_filtros(request.GET, models.Monodroga)
    mfilters = dict(filter(lambda v: v[0] in models.Monodroga.FILTROS, filters.items()))
    monodrogas = models.Monodroga.objects.filter(**mfilters)
    return render(request, "monodroga/monodrogas.html", {"monodrogas": monodrogas, "filtros": filters})

@login_required(login_url='login')
def monodroga_add(request):
    if request.method == "POST":
        form = forms.MonodrogaFormAdd(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            if '_volver' in request.POST:
                return redirect('monodrogas')
            else:
                return redirect('monodroga_add')
    else:
        form = forms.MonodrogaFormAdd()
    return render(request, "monodroga/monodrogaAdd.html", {"form": form})

@login_required(login_url='login')
def monodroga_update(request, id_monodroga):
    monodroga = get_object_or_404(models.Monodroga, pk=id_monodroga)
    if request.method == "POST":
        form = forms.MonodrogaFormUpdate(request.POST, instance=monodroga)
        if form.is_valid():
            form.save()
            return redirect('monodrogas')
    else:
        form = forms.MonodrogaFormUpdate(instance=monodroga)
    return render(request, "monodroga/monodrogaUpdate.html", {'form': form, 'id': id_monodroga})

@login_required(login_url='login')
def monodroga_delete(request, id_monodroga):
    monodroga = models.Monodroga.objects.get(pk=id_monodroga)
    monodroga.delete()
    return redirect('monodrogas')

@login_required(login_url='login')
def nombresFantasia(request):
    filters = get_filtros(request.GET, models.NombreFantasia)
    mfilters = dict(filter(lambda v: v[0] in models.NombreFantasia.FILTROS, filters.items()))
    nombresFantasias = models.NombreFantasia.objects.filter(**mfilters)
    return render(request, "nombreFantasia/nombresFantasia.html",{"nombresFantasias": nombresFantasias, "filtros": filters})

@login_required(login_url='login')
def nombresFantasia_add(request):
    if request.method == "POST":
        form = forms.NombreFantasiaFormAdd(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            if '_volver' in request.POST:
                return redirect('nombresFantasia')
            else:
                return redirect('nombreFantasia_add')
    else:
        form = forms.NombreFantasiaFormAdd()
    return render(request, "nombreFantasia/nombreFantasiaAdd.html", {"form": form})

@login_required(login_url='login')
def nombresFantasia_update(request, id_nombreFantasia):
    nombresFantasias = get_object_or_404(models.NombreFantasia, pk=id_nombreFantasia)
    if request.method == "POST":
        form = forms.NombreFantasiaFormUpdate(request.POST, instance=nombresFantasias)
        if form.is_valid():
            form.save()
            return redirect('nombresFantasia')
    else:
        form = forms.NombreFantasiaFormUpdate(instance=nombresFantasias)
    return render(request, "nombreFantasia/nombreFantasiaUpdate.html", {'form': form, 'id': id_nombreFantasia})

@login_required(login_url='login')
def nombresFantasia_delete(request, id_nombreFantasia):
    nombreFantasia = models.NombreFantasia.objects.get(pk=id_nombreFantasia)
    nombreFantasia.delete()
    return redirect('nombresFantasia')


@login_required(login_url='login')
def presentaciones(request):
    filters = get_filtros(request.GET, models.Presentacion)
    mfilters = dict(filter(lambda v: v[0] in models.Presentacion.FILTROS, filters.items()))
    presentaciones = models.Presentacion.objects.filter(**mfilters)
    return render(request, "presentacion/presentaciones.html",{"presentaciones": presentaciones, "filtros": filters})


@login_required(login_url='login')
def presentacion_add(request):
    if request.method == "POST":
        form = forms.PresentacionFormAdd(request.POST)
        if form.is_valid():
            form.save()
            if '_volver' in request.POST:
                return redirect('presentaciones')
            else:
                return redirect('presentacion_add')
    else:
        form = forms.PresentacionFormAdd()
    return render(request, "presentacion/presentacionAdd.html", {"form": form})

@login_required(login_url='login')
def presentacion_update(request, id_presentacion):
    presentacion = get_object_or_404(models.Presentacion, pk=id_presentacion)
    if request.method == "POST":
        form = forms.PresentacionFormUpdate(request.POST, instance=presentacion)
        if form.is_valid():
            form.save()
            return redirect('presentaciones')
    else:
        form = forms.PresentacionFormUpdate(instance=presentacion)
    return render(request, "presentacion/presentacionUpdate.html", {'form': form, 'id': id_presentacion})

@login_required(login_url='login')
def presentacion_delete(request, id_presentacion):
    clinica = models.Presentacion.objects.get(pk=id_presentacion)
    clinica.delete()
    return redirect('presentaciones')


@login_required(login_url='login')
def medicamentos(request):
    filters = get_filtros(request.GET, models.Medicamento)
    mfilters = dict(filter(lambda v: v[0] in models.Medicamento.FILTROS, filters.items()))
    medicamentos = models.Medicamento.objects.filter(**mfilters)
    return render(request, "medicamento/medicamentos.html", {"medicamentos": medicamentos, "filtros": filters})

@login_required(login_url='login')
def medicamento_delete(request, id_medicamento):
    medicamento = models.Medicamento.objects.get(pk= id_medicamento)
    medicamento.delete()
    return redirect('medicamentos')

@login_required(login_url='login')
def medicamento_add(request):
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
            if '_volver' in request.POST:
                return redirect('medicamentos')
            else:
                return redirect('medicamento_add')
            #redirect("medicamento_add")
    return render(request, "medicamento/medicamentoAdd.html", {
        "medicamento_form": medicamento_form,
        "dosis_formset": dosis_formset,
    })

#from django.contrib.auth import decorators as authd
@login_required(login_url='login')
#@authd.permission_required(perm="medicamentos.add_medicamento")  #codename del permiso
def medicamento_update(request, id_medicamento):
    medicamento= get_object_or_404(models.Medicamento, pk=id_medicamento)
    if request.method == "POST":
        form = forms.MedicamentoFormUpdate(request.POST, instance=medicamento)
        if form.is_valid():
            form.save()
            return redirect('medicamentos')
    else:
        form = forms.MedicamentoFormUpdate(instance=medicamento)
    return render(request, "medicamento/medicamentoUpdate.html", {'form': form, 'id': id_medicamento})

