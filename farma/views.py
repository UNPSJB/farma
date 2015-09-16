from django.shortcuts import render

def login(request):
    return render(request, "login.html")

def inicio(request):
    return render(request, "inicio.html")

def altaFarmacia(request):
	return render(request, "altaFarmacia.html")

def altaClinica(request):
	return render(request, "altaClinica.html")

def altaObraSocial(request):
	return render(request, "altaObraSocial.html")