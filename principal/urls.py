from django.urls import path

from . import views


urlpatterns  = [
    path('', views.home),
    path('<str:material>/<str:tipo>/<int:id_joya>', views.joya),
    path('login/', views.ingresar),
    path('logout/', views.salir),
    path('carro/', views.carro_compras),
]