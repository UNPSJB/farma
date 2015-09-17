from django.shortcuts import render
from  medicamentos.models import Monodroga


def get_order(get):
    if "o" in get:
        return get["o"]

def login(request):
    return render(request, "login.html")

def inicio(request):
    return render(request, "inicio.html")

def altafarmacia(request):
	return render(request, "altafarmacia.html")

def altaMedicamento(request):
	return render(request, "altaMedicamento.html")