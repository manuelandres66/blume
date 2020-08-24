from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class Entrar(forms.Form):
    usuario = forms.CharField(max_length=1000)
    password = forms.CharField(max_length=1000, widget=forms.PasswordInput)

class Envio(forms.Form):
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

    departamento = forms.ChoiceField(choices = DEPARTAMENTO)
    ciudad = forms.CharField(max_length=1000, widget=forms.TextInput(attrs={'placeholder': 'Ciudad'}))
    direccion = forms.CharField(max_length=10000, widget=forms.TextInput(attrs={'placeholder': 'Dirrección'}))
    datos_adicionales = forms.CharField(max_length=1000, widget=forms.TextInput(attrs={'placeholder': 'Datos Adicionales'}))
    telefono = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Telefóno'}))

class CrearUsuario(UserCreationForm):
    class Meta:
        fields = ('username','email','password1','password2')
        model = get_user_model()