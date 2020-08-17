from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Joya(models.Model):
    nombre = models.CharField(max_length=100000)
    MATERIAL = [
        ('oro', 'Oro'),
        ('plata', 'Plata'),
        ('otros', 'Otros')
    ]
    material = models.CharField(max_length=7, choices=MATERIAL, default='Oro')
    TIPO = [
        ('aretes', 'Arete'),
        ('pulseras', 'Pulsera'),
        ('collares', 'Collar'),
        ('anillos', 'Anillo'),
        ('otros', 'Otro')
    ]
    tipo = models.CharField(max_length=50, choices=TIPO, default='Arete')
    piedra = models.CharField(max_length=100000)
    precio = models.IntegerField()
    imagen = models.ImageField(upload_to='static/images', null=True, blank=True)
    descripcion = models.TextField()
    stock = models.IntegerField(default=1)
    vistas = models.PositiveIntegerField(default=0)

class Carrito(models.Model):
    check_out = models.BooleanField(default=False)
    propietario = models.OneToOneField(User, on_delete=models.CASCADE)

class Items(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    producto = models.ForeignKey(Joya, on_delete=models.CASCADE)

    def total(self):
        return self.cantidad * self.producto.precio

    def posible(self):
        return self.cantidad <= self.producto.stock