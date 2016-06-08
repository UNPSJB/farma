from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def get_order(get):
    if "o" in get:
        return get["o"]


@login_required(login_url='login')
def inicio(request):
    return render(request, "inicio/inicio.html")


def paginaEnConstruccion(request):
    return render(request, "paginaEnConstruccion.html")