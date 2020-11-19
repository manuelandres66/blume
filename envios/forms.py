from django.forms import ModelForm
from principal.models import Joya
from .models import Envios

class Nueva_Joya(ModelForm):
    class Meta:
        model = Joya
        fields = ['nombre', 'material', 'tipo', 'piedra', 'precio', 'imagen', 'descripcion', 'stock']

class Cambiar_Envio(ModelForm):
    class Meta:
        model = Envios
        fields = ['estado', 'llega']