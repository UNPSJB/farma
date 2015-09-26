from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.http import *
import datetime

def get_order(get):
    if "o" in get:
        return get["o"]

def inicio(request):
    return render(request, "inicio.html")

def altaFarmacia(request):
	return render(request, "altaFarmacia.html")

def altaMedicamento(request):
	return render(request, "altaMedicamento.html")

def pedidoALaboratorio(request):
  fecha = datetime.datetime.now()
  return render(request, "pedidoALaboratorio.html", {'fecha_pedido': fecha})

def recepcionPedidoDeLaboratorio(request):
  fecha = datetime.datetime.now()
  return render(request, "recepcionPedidoDeLaboratorio.html", {'fecha_pedido': fecha})

def pedidoDeFarmacia(request):
  fecha = datetime.datetime.now()
  return render(request, "pedidoDeFarmacia.html",{'fecha_pedido': fecha})

def pedidoDeClinica(request):
  fecha = datetime.datetime.now()
  return render(request, "pedidoDeClinica.html",{'fecha_pedido': fecha})
  
def altaMonodroga(request):
  return render(request, "altaMonodroga.html")  

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
               if user.is_active:
                   login(request, user)
                   return redirect('inicio')
               else:
                   return HttpResponse('inactive')
    return render(request, "login.html")
