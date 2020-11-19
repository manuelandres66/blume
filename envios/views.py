from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

import datetime
import requests as res
import json

from .forms import Nueva_Joya
from .models import Envios, Item_enviado

from principal.views import ACCESS_TOKEN
from principal.models import Joya
from principal.decorators import usuarios_validos

@usuarios_validos(rol=['administradores'])
@login_required(login_url="/login/")
def home(request):
    joyas = Joya.objects.all().order_by('-vistas')
    error = ""
    if 'numero' in request.GET:
        try:
            joyas = [Joya.objects.get(id=request.GET['numero'])]
        except:
            joyas = []
            error = "No hay joya que coincida"
    ctx = {'joyas' : joyas, 'error' : error}
    return render(request, 'envios/home_envios.html', ctx)

@usuarios_validos(rol=['administradores'])
@login_required(login_url="/login/")
def ingresar_joya(request):
    if request.method == 'POST':
        form = Nueva_Joya(request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/envios/')
            
    form  = Nueva_Joya()
    ctx = {'formulario' : form}
    return render(request, 'envios/ingresar_joyas.html', ctx)

@usuarios_validos(rol=['administradores'])
@login_required(login_url="/login/")
def envios(request):
    envio = Envios.objects.get(id=request.GET['id'])
    envios = [envio]
    todos_items = [Item_enviado.objects.filter(envio=envio)]
    ctx = {'envios' : envios, 'items' : todos_items, 'admin' : True}
    return render(request, 'pagina_envios.html', ctx)
    


@usuarios_validos(rol=['administradores'])
@login_required(login_url="/login/")
def check(request):
    envio = Envios.objects.get(id=request.GET["envio"])
    
    if envio.token is not None:
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
            if fecha.day < datetime.datetime.now().day:  # Si despues de 5 dias no se ha aprobado, cancelamos el envio
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
        if bool(resp['results'][0]['card']): #Comprobamos que si es tarjeta de credito mostramos los 4 ultimos digitos
            termina_en = resp['results'][0]['card']['last_four_digits']

        ctx = {'envio': envio, 'numero_compra': envio.token, 'tarjeta': resp['results'][0]['payment_method_id'],
            'termina_en': termina_en, 'estilo': estilo}
        return render(request, 'aprobado.html', ctx)
    else:
        return HttpResponse('Al parecer, el usuario no ha completado el envio, espera 30 minutos, si este mensaje despues de eso sigue apareciendo descarta esta notificación')