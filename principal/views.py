from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Joya
from .decorators import usuario_sin_ingresar
from .forms import Entrar
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    return render(request, 'home.html')

def joya(request, material, tipo, id_joya):
    joya_f = get_object_or_404(Joya, id=id_joya, material=material, tipo=tipo)
    precio = format(int(joya_f.precio), ',d')
    stock = "Stock Disponible"
    if joya_f.stock == 0:
        stock = "No hay stock"
    ctx = {'joya' : joya_f, 'precio' : precio, 'stock' : stock}
    return render(request, 'producto.html', ctx)

@usuario_sin_ingresar
def ingresar(request):
    error = ""
    if request.method == 'POST':
        form = Entrar(request.POST)
        if form.is_valid():
            usuario = request.POST['usuario']
            password = request.POST['password']
            user = authenticate(username=usuario, password=password)
            if user is not None:
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                return redirect('../../')
            else:
                error = "Usuario y contraseña no coinciden"
        else:
            error = "Datos Invalidos"
    form = Entrar()
    ctx = {'form' : form, 'error' : error}
    return render(request, 'login.html', ctx)

@login_required(login_url="../login/")
def salir(request):
    logout(request)
    return redirect('../../')



