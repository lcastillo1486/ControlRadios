from django.forms import ModelForm
from .models import movimientoRadios, invSeriales, entradaDetalle, buscaentregados, contable, abono_factura
from django.forms import widgets
from django import forms
from cliente.models import cliente, razonSocial
from ordenes.models import ordenRegistro


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


class FacturaPDFForm(forms.ModelForm):
    class Meta:
        model = ordenRegistro
        fields = ['factura_pdf']  # Solo queremos el campo para subir el PDF
        labels = {
            'factura_pdf' : 'Adjuntar Factura'
        }
    
    def __init__(self, *args, **kwargs):
        super(FacturaPDFForm, self).__init__(*args, **kwargs)
        self.fields['factura_pdf'].required = True  

class formRegistroMontoFact(forms.ModelForm):
    class Meta:
        model = contable
        fields = ['monto_base','igv','monto_total', 'porcentaje_detrac','detraccion']
        labels = {
            'monto_base' : 'Sub Total:',
            'igv' : 'IGV:',
            'monto_total' : 'Monto Total:',
            'detraccion' : 'Monto Detracción'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['igv'].widget.attrs['readonly'] = 'readonly'
        self.fields['monto_total']
        self.fields['detraccion'].widget.attrs['readonly'] = 'readonly'
        self.fields['monto_base'].required = True
        self.fields['igv'].required = True
        self.fields['monto_total'].required = True

class formRegistroMontoFactNoSunat(forms.ModelForm):
    class Meta:
        model = contable
        fields = ['monto_total']
        labels = {
            'monto_total' : 'Monto Total:',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['monto_total']
        
class formRegistroMontopago(forms.ModelForm):
    class Meta:
        model = contable
        fields = ['abono', 'fecha_pago','referencia_pago']
        labels = {
            'abono' : 'Monto Pagado:',
            'fecha_pago' : 'Fecha de Pago:',
            'referencia_pago' : 'Referencia:'
        }

        widgets = {
            'fecha_pago': widgets.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['abono'].required = True
        self.fields['fecha_pago'].required = True
        self.fields['referencia_pago'].required = True

class comprobantePagoForm(forms.ModelForm):
    class Meta:
        model = contable
        fields = ['comprobante_pago']  # Solo queremos el campo para subir el PDF
        labels = {
            'comprobante_pago' : 'Adjuntar Comprobante:'
        }
    
    def __init__(self, *args, **kwargs):
        super(comprobantePagoForm, self).__init__(*args, **kwargs)
        self.fields['comprobante_pago'].required = False  


class comprobanteabonoForm(forms.ModelForm):
    class Meta:
        model = abono_factura
        fields = ['comprobante_pago']  # Solo queremos el campo para subir el PDF
        labels = {
            'comprobante_pago' : 'Adjuntar Comprobante:'
        }

    
    def __init__(self, *args, **kwargs):
        super(comprobanteabonoForm, self).__init__(*args, **kwargs)
        self.fields['comprobante_pago'].required = False              
        
class rxcontroleventoform(forms.Form):
    serial = forms.CharField(max_length=100, label="Serial")

class ResponsableForm(forms.Form):
    responsable = forms.CharField(max_length=100, label="Responsable")
    telefono = forms.CharField(max_length=20, label='Teléfono', required=False)

class rxcontroleventoformRecojo(forms.Form):
    serial_recojo = forms.CharField(max_length=100, label="Serial")