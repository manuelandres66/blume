from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('nuevajoya/', views.ingresar_joya),
    path('check/', views.check),
    path('envio/', views.envios),
    path('pendientes/', views.pendientes)
]