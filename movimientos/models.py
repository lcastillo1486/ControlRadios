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
    cobras = models.PositiveIntegerField(null=True, default=0)
    baterias = models.PositiveIntegerField(null=True, default=0)
    cargadores = models.PositiveIntegerField(null=True, default=0)
    handsfree = models.PositiveIntegerField(null=True, default=0)
    cascos = models.PositiveIntegerField(null=True, default=0)
    repetidoras = models.PositiveIntegerField(null=True, default=0)
    estaciones = models.PositiveIntegerField(null=True, default=0)
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

class vista_movimiento_radios_tipos(models.Model):
    id_salida = models.CharField(max_length=150)
    serialrx = models.CharField(max_length=150)
    estado = models.CharField(max_length=150)
    tipo = models.CharField(max_length=150)
    fecha_creacion = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'vista_movimiento_radios_tipos'
        auto_created = True

class auditoria(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(blank=True, null=True)
    accion = models.CharField(max_length=200, blank=True, null=True)
    usuario = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'auditoria'

class mochila(models.Model):
    id = models.AutoField(primary_key=True)
    numero_orden = models.CharField(max_length=200)
    color = models.CharField(max_length=200)

    class Meta:
        db_table = 'colormochila'


class buscaentregados(models.Model):
    cliente = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'vista_ordenes_devueltas'
        auto_created = True


class vista_ordenes_procesadas(models.Model):
    id = models.AutoField(primary_key=True)
    fecha_creacion = models.DateTimeField(blank=True, null=True)
    fecha_entrega = models.DateTimeField(blank=True, null=True)
    fecha_evento_desde = models.DateTimeField(blank=True, null=True)
    fecha_retiro = models.DateTimeField(blank=True, null=True)
    cantidad_radios = models.CharField(max_length=150)
    cantidad_cobras = models.CharField(max_length=150)
    cantidad_baterias = models.CharField(max_length=150)
    cantidad_cargadores = models.CharField(max_length=150)
    cantidad_manos_libres = models.CharField(max_length=150)
    cantidad_cascos = models.CharField(max_length=150)
    cantidad_repetidoras = models.CharField(max_length=150)
    cantidad_estaciones = models.CharField(max_length=150)
    observaciones = models.CharField(max_length=150)
    direccion_entrega = models.CharField(max_length=150)
    fecha_evento_hasta = models.DateTimeField(blank=True, null=True)
    telefono = models.CharField(max_length=150)
    cliente = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'vista_ordenes_procesadas'
        auto_created = True

class vista_ordenes_cerradas(models.Model):
    id = models.AutoField(primary_key=True)
    fecha_creacion = models.DateTimeField(blank=True, null=True)
    fecha_entrega = models.DateTimeField(blank=True, null=True)
    fecha_evento_desde = models.DateTimeField(blank=True, null=True)
    fecha_retiro = models.DateTimeField(blank=True, null=True)
    cantidad_radios = models.CharField(max_length=150)
    cantidad_cobras = models.CharField(max_length=150)
    cantidad_baterias = models.CharField(max_length=150)
    cantidad_cargadores = models.CharField(max_length=150)
    cantidad_manos_libres = models.CharField(max_length=150)
    cantidad_cascos = models.CharField(max_length=150)
    cantidad_repetidoras = models.CharField(max_length=150)
    cantidad_estaciones = models.CharField(max_length=150)
    observaciones = models.CharField(max_length=150)
    direccion_entrega = models.CharField(max_length=150)
    fecha_evento_hasta = models.DateTimeField(blank=True, null=True)
    telefono = models.CharField(max_length=150)
    cliente = models.CharField(max_length=150)
    id_salida = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'vista_ordenes_cerradas'
        auto_created = True

class vista_entrada_detalle(models.Model):
    id = models.AutoField(primary_key=True)
    id_orden = models.CharField(max_length=150)
    fecha_creacion = models.DateField(blank=True, null=True)
    cobras = models.CharField(max_length=150)
    cargadores = models.CharField(max_length=150)
    handsfree = models.CharField(max_length=150)
    cascos = models.CharField(max_length=150)
    repetidoras = models.CharField(max_length=150)
    estaciones = models.CharField(max_length=150)
    observaciones = models.CharField(max_length=150)
    cliente = models.CharField(max_length=150)
    baterias = models.CharField(max_length=150)
    fecha_evento = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vista_entrada_detalle'
        auto_created = True





    



