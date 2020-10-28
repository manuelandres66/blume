from django.forms import ModelForm
from principal.models import Joya

class Nueva_Joya(ModelForm):
    class Meta:
        model = Joya
        fields = ['nombre', 'material', 'tipo', 'piedra', 'precio', 'imagen', 'descripcion', 'stock']
