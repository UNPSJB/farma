from django.shortcuts import render
from  medicamentos.models import Monodroga


def get_order(get):
    if "o" in get:
        return get["o"]

def get_filtros(get, modelo):
    mfilter = {}
    for filtro in modelo.FILTROS:
        attr = filtro.split("__")[0]
        if attr in get and get[attr]:
            mfilter[filtro] = get[attr]
            mfilter[attr] = get[attr]
    return mfilter

def login(request):
    return render(request, "login.html")

def inicio(request):
    return render(request, "inicio.html")

def altafarmacia(request):
	return render(request, "altafarmacia.html")

def monodrogas(request):
    filters = get_filtros(request.GET, Monodroga)
    mfilters = dict(filter(lambda v: v[0] in Monodroga.FILTROS, filters.items()))
    print("Filtros", filters)
    print("MFiltros", mfilters)
    print("Orden", get_order(request.GET))
    #monodrogas = filter(lambda m: m.upper().startswith(mfilter["nombre"].upper()), Monodrogas)
    monodrogas = Monodroga.objects.filter(**mfilters)
    #monodrogas.order_by(get_order(request.GET))
    return render(request, "monodrogas.html", {"monodrogas": monodrogas, "filtros": filters})

def altaMedicamento(request):
	return render(request, "altaMedicamento.html")