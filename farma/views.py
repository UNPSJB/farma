from django.shortcuts import render
from django.http import *
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import authenticate

def get_order(get):
    if "o" in get:
        return get["o"]

def inicio(request):
    return render(request, "inicio.html")

def altafarmacia(request):
	return render(request, "altafarmacia.html")

def altaMedicamento(request):
	return render(request, "altaMedicamento.html")

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
