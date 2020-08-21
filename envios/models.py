from django.db import models
from principal.models import Joya
import datetime
from django.contrib.auth.models import User
# Create your models here.

class Envios(models.Model):
    propietario = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    DEPARTAMENTO = [
        ('Amazonas', 'Amazonas'),
        ('Antioquia', 'Antioquia'),
        ('Arauca', 'Arauca'),
        ('Atlántico', 'Atlántico'),
        ('Bogotá', 'Bogotá'),
        ('Bolívar', 'Bolívar'),
        ('Boyacá', 'Boyacá'),
        ('Caldas', 'Caldas'),
        ('Caquetá', 'Caquetá'),
        ('Casanare', 'Casanare'),
        ('Cauca', 'Cauca'),
        ('Cesar', 'Cesar'),
        ('Chocó', 'Chocó'),
        ('Córdoba', 'Córdoba'),
        ('Cundinamarca', 'Cundinamarca'),
        ('Guainía', 'Guainía'),
        ('Guaviare', 'Guaviare'),
        ('Huila', 'Huila'),
        ('La Guajira', 'La Guajira'),
        ('Magdalena', 'Magdalena'),
        ('Meta', 'Meta'),
        ('Nariño', 'Nariño'),
        ('Norte de Santander', 'Norte de Santander'),
        ('Putumayo', 'Putumayo'),
        ('Quindío', 'Quindío'),
        ('Risaralda', 'Risaralda'),
        ('San Andrés y Providencia', 'San Andrés y Providencia'),
        ('Santander', 'Santander'),
        ('Sucre', 'Sucre'),
        ('Tolima', 'Tolima'),
        ('Valle del Cauca', 'Valle del Cauca'),
        ('Vaupés', 'Vaupés'),
        ('Vichada', 'Vichada')
    ]
    departamento = models.CharField(max_length=50, choices=DEPARTAMENTO)
    ciudad = models.CharField(max_length=1000)
    direccion = models.CharField(max_length=10000)
    datos_adicionales = models.CharField(max_length=10000)
    celular = models.IntegerField()
    llega = models.DateTimeField(default=datetime.datetime.now())

class Item_enviado(models.Model):
    envio = models.ForeignKey(Envios, on_delete=models.CASCADE)
    producto = models.ForeignKey(Joya, on_delete=models.RESTRICT)
