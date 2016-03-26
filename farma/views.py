from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
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

def logout_user(request):
    logout(request)
    return redirect('login')

def paginaEnConstruccion(request):
      return render(request, "paginaEnConstruccion.html")


