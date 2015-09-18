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

def pedidoLaboratorio(request):
	return render(request, "pedidoLaboratorio.html")

def recepcionPedidoLaboratorio(request):
	return render(request, "recepcionPedidoLaboratorio.html")

def pedidoDeFarmacia(request):
	return render(request, "pedidoDeFarmacia.html")

def pedidoDeClinica(request):
	return render(request, "pedidoDeClinica.html")
