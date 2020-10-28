from django.http import HttpResponse
from django.shortcuts import redirect

def usuario_sin_ingresar(view_func):
    def comprobador(request, *args, **kargs):
        if request.user.is_authenticated:
            if 'next' in request.GET:
                return redirect(request.GET.get('next'))
            return redirect('../../')
        else:
            return view_func(request, *args, **kargs)
    return comprobador

def usuarios_validos(rol=[]):
    def decorador(view_func):
        def comprobador_rol(request, *args, **kargs):
            grupo = None
            if request.user.groups.exists():
                grupo = request.user.groups.all()[0].name
            
            if grupo in rol:
                return view_func(request, *args, **kargs)
            else:
                return redirect('/login/')
        return comprobador_rol
    return decorador