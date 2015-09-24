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
    return render(request, "organizaciones/farmacias.html",
        {"farmacias": farmacias,
         "filtros": filters,
         "form": form})
