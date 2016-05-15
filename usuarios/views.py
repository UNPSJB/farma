from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from . import forms
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import permission_required


def get_permiso(tipoCargo):
    if tipoCargo == 'Encargado General':
        return Permission.objects.get(codename="encargado_general")

    if tipoCargo == 'Encargado Medicamentos Vencidos':
        return Permission.objects.get(codename="encargado_medicamentos_vencidos")

    if tipoCargo == 'Encargado de Stock':
        return Permission.objects.get(codename="encargado_stock")

    if tipoCargo == 'Encargado de Pedido':
        return Permission.objects.get(codename="encargado_pedido")

    if tipoCargo == 'Empleado de Despacho de Pedido':
        return Permission.objects.get(codename="empleado_despacho_pedido")


@csrf_protect
@permission_required('usuarios.encargado_general', login_url='login')
@login_required(login_url='login')
def usuario_add(request):
    if request.method == 'POST':
        form = forms.UsuarioAddForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit="False")
            usuario.user_permissions.add(get_permiso(usuario.cargo))
            usuario.set_password(form.cleaned_data['password'])
            usuario.save()
            return redirect('/')
    else:
        form = forms.UsuarioAddForm()
    return render(request, 'usuarioAdd.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = forms.UsuarioLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('inicio')
        else:
            return render(request, "login.html", {'form':form})
    else: 
        form = forms.UsuarioLoginForm()
    return render(request, "login.html", {'form':form})


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('login')
