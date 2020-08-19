from django import forms
from django.contrib.auth.models import User

class Entrar(forms.Form):
    usuario = forms.CharField(max_length=1000)
    password = forms.CharField(max_length=1000, widget=forms.PasswordInput)

class Envio(forms.Form):
    departamento = forms.CharField(max_length=1000, widget=forms.TextInput(attrs={'placeholder': 'Departamento'}))
    ciudad = forms.CharField(max_length=1000, widget=forms.TextInput(attrs={'placeholder': 'Ciudad'}))
    direccion = forms.CharField(max_length=10000, widget=forms.TextInput(attrs={'placeholder': 'Dirrección'}))
    datos_adicionales = forms.CharField(max_length=1000, widget=forms.TextInput(attrs={'placeholder': 'Datos Adicionales'}))
    telefono = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Telefóno'}))

