from django.http import HttpResponse
from django.shortcuts import redirect

def usuario_sin_ingresar(view_func):
    def comprobador(request, *args, **kargs):
        if request.user.is_authenticated:
            if 'next' in request.GET:
                return redirect(request.GET.get('next'))
            return redirect('/')
        else:
            return view_func(request, *args, **kargs)
    return comprobador