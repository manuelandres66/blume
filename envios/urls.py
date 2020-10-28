from django.urls import path
from . import views

urlpatterns = [
    path('joya/', views.ingresar_joya)
]