from django.forms import ModelForm
from .models import cliente

class formCliente(ModelForm):

    class Meta:
        model = cliente
        fields = '__all__'


