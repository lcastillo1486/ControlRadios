from django.forms import ModelForm
from .models import ordenRegistro
from cliente.models import cliente, razonSocial
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
            'cantidad_manos_libres':'Handsfree',
            'cantidad_estaciones':'Tipo Escolta',
            'cantidad_radios':'Radios',
            'cantidad_cobras':'Cobras',
            'cantidad_cascos':'Cascos',
            'cantidad_baterias':'Baterias',
            'cantidad_cargadores': 'Cargadores',
            'cantidad_repetidoras':'Repetidoras',
            'fecha_retiro':'Fecha de Recojo',
            'fecha_entrega':'Fecha de Entrega'         
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ordenar alfabéticamente el campo cliente
        self.fields['cliente'].queryset = cliente.objects.all().order_by('nombre')
        self.fields['razon_Social'].queryset = razonSocial.objects.all().order_by('denominacion')

class formEdit(ModelForm):

    class Meta:
        model = ordenRegistro
        fields = ['cliente', 'razon_Social','fecha_entrega','fecha_evento_desde','fecha_evento_hasta','fecha_retiro',
                  'cantidad_radios', 'cantidad_cobras','cantidad_manos_libres','cantidad_estaciones','cantidad_cascos',
                   'cantidad_baterias','cantidad_cargadores','cantidad_repetidoras','observaciones','direccion_entrega']
        
        labels = {
            'cantidad_manos_libres':'Handsfree',
            'cantidad_estaciones':'Tipo Escolta',
            'cantidad_radios':'Radios',
            'cantidad_cobras':'Cobras',
            'cantidad_cascos':'Cascos',
            'cantidad_baterias':'Baterias',
            'cantidad_cargadores': 'Cargadores',
            'cantidad_repetidoras':'Repetidoras',
            'fecha_retiro':'Fecha de Recojo',
            'fecha_entrega':'Fecha de Entrega'         
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ordenar alfabéticamente el campo cliente
        self.fields['cliente'].queryset = cliente.objects.all().order_by('nombre')
        self.fields['razon_Social'].queryset = razonSocial.objects.all().order_by('denominacion')

class formEditFactura(ModelForm):

    class Meta:
        model = ordenRegistro
        fields = ['cliente', 'razon_Social']
        
        labels = {
            'cliente':'Cliente:',
            'razon_Social':'Razon Social:',
                  
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ordenar alfabéticamente el campo cliente
        self.fields['cliente'].queryset = cliente.objects.all().order_by('nombre')
        self.fields['razon_Social'].queryset = razonSocial.objects.all().order_by('denominacion')
        self.fields['cliente'].disabled = True
        