from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from envios.models import Envios, Item_enviado
from .models import Joya, Carrito, Items
from .decorators import usuario_sin_ingresar
from .forms import Entrar, Envio
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import datetime

import mercadopago
import json
# Create your views here.

def home(request):
    return render(request, 'home.html') #En proceso

def joya(request, material, tipo, id_joya):
    joya_f = get_object_or_404(Joya, id=id_joya, material=material, tipo=tipo) 
    joya_f.vistas += 1 #Aumentamos una vista
    joya_f.save()

    mensaje = ""
    if request.user.is_authenticated: #Comprobamos si ya esta en el carrito
        usuario = User.objects.get(username=request.user)
        carro = Carrito.objects.get(propietario=usuario)
        productos = Items.objects.filter(carrito=carro, producto=joya_f)
        if productos.count() >= 1:
            mensaje = "Este producto ya esta en tu carro"

    precio = format(int(joya_f.precio), ',d')
    stock = "Stock Disponible" #Comprobamos si hay stock
    if joya_f.stock == 0:
        stock = "No hay stock"

    ctx = {'joya' : joya_f, 'precio' : precio, 'stock' : stock, 'mensaje' : mensaje}
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
                login(request, user) #Logeamos
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
    return redirect('../../') #A la pagina principal

@login_required(login_url="/login/")
def carro_compras(request):
    usuario = User.objects.get(username=request.user)
    carro = Carrito.objects.get(propietario=usuario)    
    if request.method == "GET":

        if 'eliminar' in request.GET: #Eliminar del carrito
            id_ = request.GET['eliminar']
            joya_item = Joya.objects.get(id=id_)
            Items.objects.filter(carrito=carro, producto=joya_item).delete()
            return redirect('/carro/')

        elif 'add' in request.GET: #Añadir al carrito
            id_ = request.GET["add"]
            joya_item = Joya.objects.get(id=id_)
            if Items.objects.filter(carrito=carro, producto=joya_item).count() == 1: #Si ya existe aumenta uno
                existente = Items.objects.get(carrito=carro, producto=joya_item)
                print(existente.cantidad, joya_item.stock)
                if existente.cantidad < joya_item.stock: #Si es posible
                    existente.cantidad += 1
                    existente.save()
            else:  
                Items(carrito=carro, cantidad=1, producto=joya_item).save()
            return redirect('/carro/')

        elif 'remove' in request.GET: #Quita uno del carrito
            id_ = request.GET["remove"]
            joya_item = Joya.objects.get(id=id_)
            menos_una = Items.objects.get(carrito=carro, producto=joya_item)
            if menos_una.cantidad > 1: # lo minimo es uno
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

    if len(productos) > 0:
        style = True
        valor_total = 0
        form = Envio()
        for producto in productos:
            if producto.posible():
                valor_total += producto.total()

        con_envio = valor_total + 16000
        url = ""

        if request.method == "POST":
            form = Envio(request.POST)
            if form.is_valid():
                # crear_envio = Envios(
                #     departamento= form.cleaned_data['departamento'],
                #     ciudad = form.cleaned_data['ciudad'],
                #     direccion = form.cleaned_data['direccion'],
                #     datos_adicionales= form.cleaned_data['datos_adicionales'],
                #     celular = form.cleaned_data['telefono'],
                #     llega = datetime.datetime.now() + datetime.timedelta(days=5)
                # )
                # crear_envio.save()
                # for producto in productos:
                #     producto.producto.stock -= producto.cantidad
                #     producto.producto.save()
                #     Item_enviado(envio=crear_envio, producto=producto.producto).save()

                # carro.delete()
                # Carrito(check_out=False, propietario=usuario).save() #Creando un carrito vacio

                style = False
                preference = {
                    "items": [
                        {
                            'title' : "Total Blume",
                            'quantity' : 1,
                            "currency_id": "COP",
                            "unit_price" : con_envio
                        }
                    ]
                }

                mp = mercadopago.MP("TEST-2491172127206962-082115-73f07ae6a3250046a24679600ffd8bba-18920383")
                preferenceResult = mp.create_preference(preference)
                url = preferenceResult["response"]["init_point"]

                carro.check_out = True
                carro.save()
                # productos = Item_enviado.objects.filter(envio=crear_envio)
        

        ctx = {'subtotal' : valor_total, 'total' : con_envio, 'productos' : productos, 'style' : style, 'form' : form, 'url' : url}
        return render(request, 'checkout.html', ctx)

    else:
        return redirect('/carro')

@login_required(login_url="/login/")
def aproved(request):
    pass