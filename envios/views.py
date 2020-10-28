from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .forms import Nueva_Joya

from principal.models import Joya
from principal.decorators import usuarios_validos

@usuarios_validos(rol=['administradores'])
@login_required(login_url="/login/")
def ingresar_joya(request):
    if request.method == 'POST':
        form = Nueva_Joya(request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse("""<h1>Tu joya a sido guardada</h1>
            <a href="/envios/joya/">Entra a este link para ingresar otra</a>""")
            
    form  = Nueva_Joya()
    ctx = {'formulario' : form}
    return render(request, 'envios/ingresar_joyas.html', ctx)