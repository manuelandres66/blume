from django.forms import ModelForm
from principal.models import Joya
from .models import Envios
from django import forms

class Nueva_Joya(ModelForm):
    class Meta:
        model = Joya
        fields = ['nombre', 'material', 'tipo', 'piedra', 'precio', 'imagen', 'descripcion', 'stock']

class Cambiar_Envio(forms.Form):
    ESTADOS = [
        ('Completado', 'Completado'),
        ('En envio', 'En envio'),
        ('Para entregar', 'Para entregar'),
        ('Retrasado', 'Retrasado')
    ]
    estado = forms.ChoiceField(choices = ESTADOS)
    llega = forms.DateTimeField()