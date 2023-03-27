from django.forms import ModelForm
from .models import ordenRegistro
from django.forms import widgets

class formOrden(ModelForm):

    class Meta:
        model = ordenRegistro
        exclude = ('estado',) 
        fields = '__all__'
        widgets = {
            'fecha_entrega': widgets.DateInput(attrs={'type': 'date'}),
            'fecha_evento_desde': widgets.DateInput(attrs={'type': 'date'}),
            'fecha_evento_hasta': widgets.DateInput(attrs={'type': 'date'}),
            'fecha_retiro': widgets.DateInput(attrs={'type': 'date'})
        }

class formEdit(ModelForm):

    class Meta:
        model = ordenRegistro
        fields = '__all__'
        