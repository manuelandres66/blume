from django.urls import path
from . import views

urlpatterns = [
    path('joya/', views.ingresar_joya),
    path('check/', views.check),
    path('envio/', views.envios)
]