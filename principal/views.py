from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Joya, Carrito, Items
from .decorators import usuario_sin_ingresar
from .forms import Entrar
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.

def home(request):
    return render(request, 'home.html')

def joya(request, material, tipo, id_joya):
    joya_f = get_object_or_404(Joya, id=id_joya, material=material, tipo=tipo)
    joya_f.vistas += 1
    joya_f.save()
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
                return redirect('/')
            else:
                error = "Usuario y contraseña no coinciden"
        else:
            error = "Datos Invalidos"
    form = Entrar()
    ctx = {'form' : form, 'error' : error}
    return render(request, 'login.html', ctx)

@login_required(login_url="/login/")
def salir(request):
    logout(request)
    return redirect('../../')

@login_required(login_url="/login/")
def carro_compras(request):
    usuario = User.objects.get(username=request.user)
    carro = Carrito.objects.get(propietario=usuario)
    if request.method == "GET":

        if 'eliminar' in request.GET:
            id_ = request.GET['eliminar']
            joya_item = Joya.objects.get(id=id_)
            Items.objects.filter(carrito=carro, producto=joya_item).delete()
            return redirect('/carro/')

        elif 'add' in request.GET:
            id_ = request.GET["add"]
            joya_item = Joya.objects.get(id=id_)
            if Items.objects.filter(carrito=carro, producto=joya_item).count() == 1:
                existente = Items.objects.get(carrito=carro, producto=joya_item)
                existente.cantidad += 1
                existente.save()
            else:  
                Items(carrito=carro, cantidad=1, producto=joya_item).save()
            return redirect('/carro/')

        elif 'remove' in request.GET:
            id_ = request.GET["remove"]
            joya_item = Joya.objects.get(id=id_)
            menos_una = Items.objects.get(carrito=carro, producto=joya_item)
            if menos_una.cantidad > 1:
                menos_una.cantidad -= 1
                menos_una.save()
            return redirect('/carro/')

    productos = Items.objects.filter(carrito=carro)
    ctx = {'productos' : productos}
    return render(request, 'carrito.html', ctx)

@login_required(login_url="/login/")
def checkout(request):
    usuario = User.objects.get(username=request.user)
    carro = Carrito.objects.get(propietario=usuario)
    productos = Items.objects.filter(carrito=carro)

    valor_total = 0
    for producto in productos:
        valor_total += producto.producto.precio

    return HttpResponse('$' + format(valor_total, ',d'))
