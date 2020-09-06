from django.db import models
from principal.models import Joya
import datetime
from django.contrib.auth.models import User
import django.utils as utils
# Create your models here.

class Envios(models.Model):
    propietario = models.ForeignKey(User, on_delete=models.CASCADE)
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
    departamento = models.CharField(max_length=500, choices=DEPARTAMENTO)
    ciudad = models.CharField(max_length=10000)
    direccion = models.CharField(max_length=100000)
    datos_adicionales = models.CharField(max_length=100000)
    celular = models.BigIntegerField()
    fecha_pedido = models.DateTimeField(default=utils.timezone.now)
    llega = models.DateTimeField(default=utils.timezone.now)
    valor_total = models.IntegerField()
    token = models.IntegerField(blank=True, null=True)
    completado = models.BooleanField(default=False)

class Item_enviado(models.Model):
    envio = models.ForeignKey(Envios, on_delete=models.CASCADE)
    producto = models.ForeignKey(Joya, on_delete=models.CASCADE)
