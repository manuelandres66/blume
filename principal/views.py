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


#Diseño, No mucha Logica.
def home(request):
    joyas = Joya.objects.all().order_by('vistas')

    ctx = {'joyas': joyas}
    return render(request, 'home.html', ctx)  # En proceso

def oro(request):
    joyas = Joya.objects.get(material='oro').order_by('vistas')
    ctx = {'joyas': joyas}
    return render(request, 'home.html', ctx)

def plata(request):
    joyas = Joya.objects.get(material='plata').order_by('vistas')
    ctx = {'joyas': joyas}
    return render(request, 'home.html', ctx)




#Logica
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
def comprar_ahora(request):
    usuario = User.objects.get(username=request.user)
    carro = Carrito.objects.get(propietario=usuario)
    id_ = request.GET['joya']
    joya_item = Joya.objects.get(id=id_)
    if Items.objects.filter(carrito=carro, producto=joya_item).count() == 1:
        existente = Items.objects.get(
            carrito=carro, producto=joya_item)
        if existente.cantidad < joya_item.stock:  # Si es posible
            existente.cantidad += 1
            existente.save()
    else:
        Items(carrito=carro, cantidad=1, producto=joya_item).save()
    return redirect('/checkout')


@login_required(login_url="/login/")
def checkout(request):
    usuario = User.objects.get(username=request.user)
    carro = Carrito.objects.get(propietario=usuario)
    productos = Items.objects.filter(carrito=carro)

    # Comprando que el carro no este vacio
    if len(productos) > 0:
        style = True
        form = Envio()

        valor_total = 0
        for producto in productos:
            if producto.posible():
                valor_total += producto.total()  # Calculando el total
            else:
                producto.delete()  # Eliminamos del carro si no hay stock

        con_envio = valor_total + 16000
        id_ = 0

        if request.method == "POST":
            form = Envio(request.POST)

            if form.is_valid():
                style = False
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
                id_ = crear_envio.id

        ctx = {'subtotal': valor_total, 'total': con_envio,
               'productos': productos, 'form': form, 'style': style, 'id': id_}

        return render(request, 'checkout.html', ctx)

    else:
        return redirect('/carro')


ACCESS_TOKEN = "TEST-7015827786312976-082121-23bfc9a07e3866546d30a2b05c67cebb-629488757"


@login_required(login_url="/login/")
def tarjeta(request):
    usuario = User.objects.get(username=request.user)
    envio = Envios.objects.get(
        id=request.GET["envio"], completado=False, propietario=usuario)
    carro = Carrito.objects.get(propietario=usuario)
    productos = Items.objects.filter(carrito=carro)

    if request.method == "POST":

        URL = "https://api.mercadopago.com/v1/payments?access_token={}".format(ACCESS_TOKEN)
        headers = {
            'content-type': 'application/json',
            'accept': 'application/json',
        }

        conten = {
            'transaction_amount': envio.valor_total,
            "net_amount": envio.valor_total - 500,
            "taxes": [{
                "value": 500,
                "type": "IVA"
            }],
            'token': request.POST['token'],
            'description': "Pago total blume",
            'installments': 1,
            'payment_method_id': request.POST['payment_method_id'],
            'payer': {
                "email": request.POST["email"]
            }
        }

        conten = json.dumps(conten)
        resp = res.post(URL, data=conten, headers=headers, auth=False)
        resp = json.loads(resp.text)

        # agregando token
        envio.token = resp['id']
        envio.save()

        if resp["status"] == "approved":
            for producto in productos:
                producto.producto.stock -= producto.cantidad
                producto.producto.save()
                Item_enviado(envio=envio, producto=producto.producto).save()

            # Completando el envio
            envio.completado = True
            envio.token = resp['id']
            envio.save()

            # Creando un carrito vacio
            carro.delete()
            Carrito(check_out=False, propietario=usuario).save()

        return redirect('/checkout/check/?envio={}'.format(envio.id))

    ctx = {'total': envio.valor_total}
    return render(request, 'tarjeta.html', ctx)


@login_required(login_url="/login/")
def ticket(request, tipo):
    usuario = User.objects.get(username=request.user)
    envio = Envios.objects.get(
        id=request.GET["envio"], completado=False, propietario=usuario)
    carro = Carrito.objects.get(propietario=usuario)
    productos = Items.objects.filter(carrito=carro)

    URL = "https://api.mercadopago.com/v1/payments?access_token={}".format(ACCESS_TOKEN)
    headers = {
        'Content-Type': 'application/json'
    }

    conten = {
        'transaction_amount': envio.valor_total,
        'description': "Pago blume",
        'payment_method_id': tipo,
        'payer': {'email': usuario.email}
    }

    conten = json.dumps(conten)
    resp = res.post(URL, data=conten, headers=headers)
    resp = json.loads(resp.text)

    # Agregando token
    envio.token = resp['id']
    envio.save()

    if resp['status'] == 'pending':
        for producto in productos:
            producto.producto.stock -= producto.cantidad
            producto.producto.save()
            Item_enviado(envio=envio, producto=producto.producto).save()

        # Creando un carrito vacio
        carro.delete()
        Carrito(check_out=False, propietario=usuario).save()

        return redirect(resp['transaction_details']['external_resource_url'])
    else:
        return redirect('/checkout/check/?envio={}'.format(envio.id))


@login_required(login_url="/login/")
def check(request):
    usuario = User.objects.get(username=request.user)
    envio = Envios.objects.get(id=request.GET["envio"], propietario=usuario)

    # Solicitamos estado de un pago por id
    URL = "https://api.mercadopago.com/v1/payments/search?access_token={}&id={}".format(ACCESS_TOKEN, envio.token)
    resp = res.get(URL)
    resp = json.loads(resp.text)

    if resp['results'][0]['status'] == 'approved':
        estilo = 1
        envio.completado = True
        envio.save()

    elif resp['results'][0]['status'] == 'pending' or resp['results'][0]['status'] == 'in_process':
        fecha = envio.fecha_pedido + datetime.timedelta(days=5)
        if fecha.day == datetime.datetime.now().day:  # Si despues de 5 dias no se ha aprobado, cancelamos el envio
            URL = "https://api.mercadopago.com/v1/payments/{}?access_token={}".format(envio.token, ACCESS_TOKEN)
            headers = {
                'Content-Type': 'application/json'
            }
            conten = {"status": "cancelled"}
            conten = json.dumps(conten)
            res.put(URL, headers=headers, data=conten)

        estilo = 2
        envio.completado = False
        envio.save()

    else:
        estilo = 3
        envio.completado = False
        envio.save()

    termina_en = '0000'
    if bool(resp['results'][0]['card']):
        termina_en = resp['results'][0]['card']['last_four_digits']

    ctx = {'envio': envio, 'numero_compra': envio.token, 'tarjeta': resp['results'][0]['payment_method_id'],
           'termina_en': termina_en, 'estilo': estilo}
    return render(request, 'aprobado.html', ctx)
