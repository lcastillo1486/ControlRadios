from django.forms import ModelForm
from .models import movimientoRadios, invSeriales, entradaDetalle, buscaentregados
from django.forms import widgets
from django import forms
from cliente.models import cliente, razonSocial


class radiotipos(ModelForm):

    class Meta:
        model = movimientoRadios
        fields = ['id_tipo', 'serial']
        labels = {
            'id_tipo':'tipo',
            'serial': 'Serial'
        }


class agregarInven(ModelForm):
    class Meta:
        model = invSeriales
        fields = '__all__'
        labels = {
            'codigo':'Serial',
            'estado_id':'Estado',
            'tipo_id':'Tipo'
        } 

class formBuscaRadio(forms.Form):
    serial = forms.CharField()

class guardaEntradaRx(ModelForm):
    class Meta:
        model = movimientoRadios
        fields = ['serial']
        labels = {
            'serial': 'Serial'
        }

class formEntradaDetalle(ModelForm):
    class Meta:
        model = entradaDetalle
        fields =  ['cobras','handsfree','estaciones','cascos','baterias','cargadores','repetidoras','observaciones']
        labels = {
            'cobras':'Cobras',
            'handsfree': 'HandsFree',
            'estaciones':'Handsfree Tipo Escolta',
            'cascos':'Cascos',
            'baterias':'Baterias',
            'cargadores':'Cargadores',
            'repetidoras':'Repetidoras',
            'observaciones':'Observaciones'
        }    
       

class formBuscarInformes(forms.Form):
    cliente = forms.ModelChoiceField(queryset=cliente.objects.all(), label='Cliente')
    # rsocial = forms.ModelChoiceField(queryset=razonSocial.objects.all(),label='Razón Social')
    fechaBInformeDesde = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}), label='Desde:')
    fechaBInformeHasta = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}), label='Hasta:')            
        
