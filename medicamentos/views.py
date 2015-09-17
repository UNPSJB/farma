from django.shortcuts import render, redirect
from . import models
from . import forms
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
