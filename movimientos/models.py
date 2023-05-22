from django.db import models
from ordenes.models import ordenRegistro, cliente
from django.utils import timezone
import pytz

def obtener_fecha_hora_peru():
    peru_timezone = pytz.timezone('America/Lima')
    return timezone.now().astimezone(peru_timezone)
# Create your models here.

class salidasDetalle(models.Model):
    id_orden = models.PositiveIntegerField(null=False)
    fecha_creacion = models.DateTimeField(default=obtener_fecha_hora_peru, editable=False, blank=True, null=True)
    cobras = models.PositiveIntegerField(null=False, default=0)
    baterias = models.PositiveIntegerField(null=False, default=0)
    cargadores = models.PositiveIntegerField(null=False, default=0)
    handsfree = models.PositiveIntegerField(null=False, default=0)
    cascos = models.PositiveIntegerField(null=False, default=0)
    repetidoras = models.PositiveIntegerField(null=False, default=0)
    estaciones = models.PositiveIntegerField(null=False, default=0)

class tipoRadios(models.Model):
    tipo = models.CharField(max_length=20)


    def __str__(self):
        return self.tipo

class movimientoRadios(models.Model):
    id_tipo = models.ForeignKey(tipoRadios, on_delete=models.DO_NOTHING)
    id_salida = models.PositiveIntegerField()
    serial = models.CharField(max_length=15)
    estado = models.CharField(max_length=15)
    fecha_creacion = models.DateTimeField(default=obtener_fecha_hora_peru, editable=False, blank=True, null=True)

class estadoRadios(models.Model):
    estado = models.CharField(max_length=15)

    def __str__(self):
        return self.estado

class invSeriales(models.Model):
    codigo = models.CharField(max_length=6, unique= True)
    estado = models.ForeignKey(estadoRadios, on_delete=models.DO_NOTHING)
    tipo = models.ForeignKey(tipoRadios, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.codigo
    
class entradaDetalle(models.Model):
    id_salida = models.PositiveIntegerField(null=False)
    id_orden = models.PositiveIntegerField(null=False)
    cliente = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(default=obtener_fecha_hora_peru, editable=False, blank=True, null=True)
    cobras = models.PositiveIntegerField(null=True)
    baterias = models.PositiveIntegerField(null=True)
    cargadores = models.PositiveIntegerField(null=True)
    handsfree = models.PositiveIntegerField(null=True)
    cascos = models.PositiveIntegerField(null=True)
    repetidoras = models.PositiveIntegerField(null=True)
    estaciones = models.PositiveIntegerField(null=True)
    observaciones = models.TextField (blank = True)

class accesoriosFaltantes(models.Model):
    id_salida = models.PositiveIntegerField(null=False)
    fcobras = models.PositiveIntegerField(null=True)
    fbaterias = models.PositiveIntegerField(null=True)
    fcargadores = models.PositiveIntegerField(null=True)
    fhandsfree = models.PositiveIntegerField(null=True)
    fcascos = models.PositiveIntegerField(null=True)
    frepetidoras = models.PositiveIntegerField(null=True)
    festaciones = models.PositiveIntegerField(null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class radiosFantantes(models.Model):
    id_salida = models.PositiveIntegerField(null=False)
    fserial = models.CharField(max_length=15)

class vista_radios_faltantes(models.Model):
    n_serial = models.CharField(max_length=150)
    cod_salida = models.CharField(primary_key=True,max_length=150)
    nombre = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'vista_radios_faltantes'
        auto_created = True

class vista_accesorios_faltantes(models.Model):
    cobras = models.CharField(max_length=150)
    baterias = models.CharField(max_length=150)
    cargadores = models.CharField(max_length=150)
    handsfree = models.CharField(max_length=150)
    cascos = models.CharField(max_length=150)
    repetidoras = models.CharField(max_length=150)
    estaciones = models.CharField(max_length=150)
    cod_salida = models.CharField(primary_key=True, max_length=150)
    nombre = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'vista_accesorios_faltantes'
        auto_created = True




    



