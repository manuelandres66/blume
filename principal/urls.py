from django.urls import path

from . import views


urlpatterns  = [
    path('', views.home),
    path('joya/', views.productos),
    path('joya/<str:material>/<str:tipo>/<int:id_joya>/', views.joya),
    path('joya/<str:material>/', views.oro),

    path('login/', views.ingresar),
    path('login/cuenta_nueva/', views.nueva_cuenta),
    path('logout/', views.salir),

    path('carro/', views.carro_compras),
    path('carro/ahora/', views.comprar_ahora),

    path('checkout/', views.checkout),
    path('checkout/tarjeta/', views.tarjeta),
    path('checkout/pse/', views.pse),
    path('checkout/ticket/<str:tipo>/', views.ticket),
    path('checkout/check/', views.check),

    path('tusenvios/', views.pagina_envios),
    path('terminos_condiciones/', views.condiciones),
    path('sobre_nosotros/', views.nostros)
]