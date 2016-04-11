from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import *
import datetime

def get_order(get):
    if "o" in get:
        return get["o"]

@login_required(login_url='login')
def inicio(request):
    return render(request, "inicio/inicio.html")

@login_required(login_url='login')
def pedidoDeClinica(request):
  fecha = datetime.datetime.now()
  return render(request, "pedidoDeClinica.html",{'fecha_pedido': fecha})

@login_required(login_url='login')
def recepcionReemplazoMedicamentos(request):
  fecha = datetime.datetime.now()
  return render(request, "recepcionReemplazoMedicamentos.html",{'fecha_pedido': fecha})

@login_required(login_url='login')
def altaMonodroga(request):
  return render(request, "altaMonodroga.html")  


def paginaEnConstruccion(request):
      return render(request, "paginaEnConstruccion.html")


