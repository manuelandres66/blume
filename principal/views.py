
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from envios.models import Envios, Item_enviado
from .models import Joya, Carrito, Items
from .decorators import usuario_sin_ingresar
from .forms import Entrar, Envio, CrearUsuario
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# librerias externas
import datetime
import requests as res
import json

# Create your views here.


def home(request):
    return render(request, 'home.html')  # En proceso


def joya(request, material, tipo, id_joya):
    joya_f = get_object_or_404(Joya, id=id_joya, material=material, tipo=tipo)
    joya_f.vistas += 1  # Aumentamos una vista
    joya_f.save()

    mensaje = ""
    if request.user.is_authenticated:  # Comprobamos si ya esta en el carrito
        usuario = User.objects.get(username=request.user)
        carro = Carrito.objects.get(propietario=usuario)
        productos = Items.objects.filter(carrito=carro, producto=joya_f)
        if productos.count() >= 1:
            mensaje = "Este producto ya esta en tu carro"

    precio = format(int(joya_f.precio), ',d')
    stock = "Stock Disponible"  # Comprobamos si hay stock
    if joya_f.stock == 0:
        stock = "No hay stock"

    ctx = {'joya': joya_f, 'precio': precio,
           'stock': stock, 'mensaje': mensaje}
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
                login(request, user)  # Logeamos
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                return redirect('/')
            else:
                error = "Usuario y contraseña no coinciden"
        else:
            error = "Datos Invalidos"
    form = Entrar()
    ctx = {'form': form, 'error': error}
    return render(request, 'login.html', ctx)


@login_required(login_url="/login/")
def salir(request):
    logout(request)
    return redirect('../../')  # A la pagina principal


@usuario_sin_ingresar
def nueva_cuenta(request):
    form = CrearUsuario()

    if request.method == 'POST':
        form = CrearUsuario(request.POST)
        if form.is_valid():
            usuario = User.objects.create_user(
                username=form.cleaned_data['username'], email=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            usuario.save()
            Carrito(propietario=usuario).save()
            return redirect('/login/')

    ctx = {'form': form}
    return render(request, 'nueva_cuenta.html', ctx)


@login_required(login_url="/login/")
def carro_compras(request):
    usuario = User.objects.get(username=request.user)
    carro = Carrito.objects.get(propietario=usuario)
    if request.method == "GET":

        if 'eliminar' in request.GET:  # Eliminar del carrito
            id_ = request.GET['eliminar']
            joya_item = Joya.objects.get(id=id_)
            Items.objects.filter(carrito=carro, producto=joya_item).delete()
            return redirect('/carro/')

        elif 'add' in request.GET:  # Añadir al carrito
            id_ = request.GET["add"]
            joya_item = Joya.objects.get(id=id_)
            # Si ya existe aumenta uno
            if Items.objects.filter(carrito=carro, producto=joya_item).count() == 1:
                existente = Items.objects.get(
                    carrito=carro, producto=joya_item)
                print(existente.cantidad, joya_item.stock)
                if existente.cantidad < joya_item.stock:  # Si es posible
                    existente.cantidad += 1
                    existente.save()
            else:
                Items(carrito=carro, cantidad=1, producto=joya_item).save()
            return redirect('/carro/')

        elif 'remove' in request.GET:  # Quita uno del carrito
            id_ = request.GET["remove"]
            joya_item = Joya.objects.get(id=id_)
            menos_una = Items.objects.get(carrito=carro, producto=joya_item)
            if menos_una.cantidad > 1:  # lo minimo es uno
                menos_una.cantidad -= 1
                menos_una.save()
            return redirect('/carro/')

    productos = Items.objects.filter(carrito=carro)
    ctx = {'productos': productos}
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
            else:
                producto.delete()

        con_envio = valor_total + 16000
        url = ""

        if request.method == "POST":
            form = Envio(request.POST)
            if form.is_valid():
                crear_envio = Envios(
                    propietario=usuario,
                    departamento=form.cleaned_data['departamento'],
                    ciudad=form.cleaned_data['ciudad'],
                    direccion=form.cleaned_data['direccion'],
                    datos_adicionales=form.cleaned_data['datos_adicionales'],
                    celular=form.cleaned_data['telefono'],
                    llega=datetime.datetime.now() + datetime.timedelta(days=5),
                    valor_total=con_envio
                )

                crear_envio.save()

                # El boton del HTML solo es submit para el formulario este redirreciona
                return redirect('/checkout/tarjeta')

        ctx = {'subtotal': valor_total, 'total': con_envio,
               'productos': productos, 'form': form}

        return render(request, 'checkout.html', ctx)

    else:
        return redirect('/carro')


def hacer_post(total, token, payment_method_id, email):  # Pedir información del envio

    URL = "https://api.mercadopago.com/v1/payments?access_token=TEST-7015827786312976-082121-23bfc9a07e3866546d30a2b05c67cebb-629488757"
    headers = {
        'content-type': 'application/json',
        'accept': 'application/json',
    }

    conten = {
        'transaction_amount': total,
        "net_amount": total - 500,
        "taxes": [{
            "value": 500,
            "type": "IVA"
        }],
        'token': token,
        'description': "Pago total blume",
        'installments': 1,
        'payment_method_id': payment_method_id,
        'payer': {
            "email": email
        }
    }

    conten = json.dumps(conten)
    resp = res.post(URL, data=conten, headers=headers, auth=False)
    resp = json.loads(resp.text)
    return resp


@login_required(login_url="/login/")
def tarjeta(request):
    usuario = User.objects.get(username=request.user)
    envio = Envios.objects.filter(propietario=usuario, completado=False).order_by('-id')
    envio = envio[0]
    carro = Carrito.objects.get(propietario=usuario)
    productos = Items.objects.filter(carrito=carro)

    if request.method == "POST":

        resp = hacer_post(envio.valor_total, request.POST['token'], request.POST['payment_method_id'], request.POST["email"])
        return HttpResponse(json.dumps(resp, indent=4))
        if resp["status"] == "approved":
            for producto in productos:
                producto.producto.stock -= producto.cantidad
                producto.producto.save()
                Item_enviado(envio=envio, producto=producto.producto).save()

            #Completando el envio
            envio.completado = True
            envio.save()
            
            # Creando un carrito vacio
            carro.delete()
            Carrito(check_out=False, propietario=usuario).save()

            ctx = {'envio' : envio, 'numero_compra' : 45, 'tarjeta' : 'visa',  'banco' : 'Itaú'}
            return render(request, 'aprobado.html', ctx)

        elif resp["status"] == "in_process":
            return HttpResponse("Verificando transacción")
        else:
            return HttpResponse("Denegado")

    ctx = {'total': envio.valor_total}
    return render(request, 'tarjeta.html', ctx)
