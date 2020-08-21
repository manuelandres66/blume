from django.urls import path

from . import views


urlpatterns  = [
    path('', views.home),
    path('<str:material>/<str:tipo>/<int:id_joya>/', views.joya),
    path('login/', views.ingresar),
    path('logout/', views.salir),
    path('carro/', views.carro_compras),
    path('checkout/', views.checkout),
    path('checkout/tarjeta')
    path('checkout/procesar_pago/', views.procesar_pago)
]