from django.forms import ModelForm
from .models import ordenRegistro
from django.forms import widgets

class formOrden(ModelForm):

    class Meta:
        model = ordenRegistro
        exclude = ('estado',) 
        fields = ['cliente', 'razon_Social','fecha_entrega','fecha_evento_desde','fecha_evento_hasta','fecha_retiro',
                  'cantidad_radios', 'cantidad_cobras','cantidad_manos_libres','cantidad_estaciones','cantidad_cascos',
                   'cantidad_baterias','cantidad_cargadores','cantidad_repetidoras','observaciones','direccion_entrega']
        widgets = {
            'fecha_entrega': widgets.DateInput(attrs={'type': 'date'}),
            'fecha_evento_desde': widgets.DateInput(attrs={'type': 'date'}),
            'fecha_evento_hasta': widgets.DateInput(attrs={'type': 'date'}),
            'fecha_retiro': widgets.DateInput(attrs={'type': 'date'})
        }

        labels = {
            'cantidad_manos_libres':'Cantidad Handsfree',
            'cantidad_estaciones':'Cantidad HandsFree Tipo Escolta'
        }

class formEdit(ModelForm):

    class Meta:
        model = ordenRegistro
        fields = ['cliente', 'razon_Social','fecha_entrega','fecha_evento_desde','fecha_evento_hasta','fecha_retiro',
                  'cantidad_radios', 'cantidad_cobras','cantidad_manos_libres','cantidad_estaciones','cantidad_cascos',
                   'cantidad_baterias','cantidad_cargadores','cantidad_repetidoras','observaciones','direccion_entrega']
        labels = {
            'cantidad_manos_libres':'Cantidad Handsfree',
            'cantidad_estaciones':'Cantidad HandsFree Tipo Escolta'
        }
        