from django.db import models
from ordenes.models import ordenRegistro, cliente
from django.utils import timezone
import pytz
from django.core.validators import RegexValidator

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
    id_orden = models.CharField(max_length=150)
    serialrx = models.CharField(max_length=150)
    estado = models.CharField(max_length=150)
    tipo = models.CharField(max_length=150)
    fecha_creacion = models.CharField(max_length=150)
    cliente = models.CharField(max_length=250)
    razon_social = models.CharField(max_length=250)
    fecha_salida = models.DateField(max_length=150)
    fecha_normal= models.DateField(max_length=150)

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
    color = models.CharField(max_length=200, blank=True, null=True)

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

class contable(models.Model):
    id = models.AutoField(primary_key=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    id_salida = models.PositiveIntegerField(blank=True,null=True)
    id_orden = models.PositiveIntegerField( blank=True,null=True)
    monto_base = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    igv = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    abono = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    porcentaje_detrac = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    detraccion = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null= True)
    fecha_pago = models.DateField(blank=True, null=True)
    referencia_pago = models.CharField(max_length=50, blank=True, null=True)
    pagado = models.BooleanField(default=False)
    comprobante_pago = models.FileField(upload_to='pdfs/', null=True, blank=True)
    sunat = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'contable'
        auto_created = True


#modelo del abono

class abono_factura(models.Model):
    id = models.AutoField(primary_key=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    id_orden = models.PositiveIntegerField(null=False)
    id_salida = models.PositiveIntegerField(null=False)
    monto_abono = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_abono =  models.DateField(blank=True, null=True)
    referencia_abono = models.CharField(max_length=50, blank=True, null=True)
    comprobante_pago = models.FileField(upload_to='pdfs/', null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'abono_factura'
        auto_created = True

class vista_ordenes_cxc(models.Model):
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
    ruc = models.CharField(max_length=50)
    razon_social = models.CharField(max_length=150)
    ruc_razon_social = models.CharField(max_length=50)
    id_salida = models.CharField(max_length=150)
    id_orden = models.CharField(max_length=150)
    facturado = models.BooleanField(default=False)
    factura_pdf = models.CharField(max_length=50)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    monto_base = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    igv = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    abono = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fecha_pago = models.DateField(blank=True, null=True)
    referencia = models.CharField(max_length=50, blank=True, null=True)
    comprobante_pago = models.CharField(max_length=50)
    pagado = models.BooleanField(default=False)
    


    class Meta:
        managed = False
        db_table = 'vista_ordenes_cxc'
        auto_created = True
    
class controlrxevent(models.Model):
    id = models.AutoField(primary_key=True)
    id_salida = models.PositiveIntegerField(null=True, blank=True)
    serial = models.CharField(max_length=50, null=True, blank=True)
    responsable = models.CharField(max_length=200, null=True, blank=True)
    estadorx = models.CharField(max_length=5, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    hora = models.TimeField(null=True, blank=True)
    hora_entrega = models.TimeField(null=True, blank=True)
    dia = models.PositiveIntegerField(null=True, blank=True)
    responsable_bk = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'controlrxevent'
        auto_created = True

class controlrx_event_dia(models.Model):
    id = models.AutoField(primary_key=True)
    id_salida = models.PositiveIntegerField(null=True, blank=True)
    dia = models.PositiveIntegerField(null=True, blank=True)
    activo = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'controlrx_event_dia'
        auto_created = True

class espejo_dia_control_rx(models.Model):
    id = models.AutoField(primary_key=True)
    id_salida = models.PositiveIntegerField(null=True, blank=True)
    serial = models.CharField(max_length=50, null=True, blank=True)
    responsable = models.CharField(max_length=200, null=True, blank=True)
    estadorx = models.CharField(max_length=5, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    hora = models.TimeField(null=True, blank=True)
    hora_entrega = models.TimeField(null=True, blank=True)
    dia = models.PositiveIntegerField(null=True, blank=True)
    responsable_bk = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'espejo_dia_control_rx'
        auto_created = True

class CajasMikrot(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, null=True, blank=True)
    ip = models.CharField(max_length=20, null=True, blank=True)
    ubicacion = models.CharField(max_length=50, null=True, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = 'CajasMikrot'
        auto_created = True 

    def __str__(self):
        return self.nombre

class controlinventario(models.Model):
    id = models.AutoField(primary_key=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_cierre = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'controlinventario'
        auto_created = True

class espejo_inventario_ant(models.Model):
    id = models.AutoField(primary_key=True)
    id_inventario = models.IntegerField(blank=True, null=True)
    codigo = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(max_length=50,blank=True, null=True)
    tipo = models.CharField(max_length=50,blank=True, null=True)
    escaneado = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'espejo_inventario_ant'
        auto_created = True 

class espejo_inventario_desp(models.Model):
    id = models.AutoField(primary_key=True)
    id_inventario = models.IntegerField(blank=True, null=True)
    codigo = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(max_length=50,blank=True, null=True)
    tipo = models.CharField(max_length=50,blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'espejo_inventario_desp'
        auto_created = True


class inv_accesorios(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    cantidad = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        managed = False
        db_table = 'inv_accesorios'
        auto_created = True

    def __str__(self):
        return self.descripcion


class entrada_salida_acce(models.Model):
    id = models.AutoField(primary_key=True)
    id_item = models.CharField(max_length=2, blank=True, null=True)
    cantidad = models.IntegerField(blank=True, null=True, default=0)
    tipo_mov = models.CharField(max_length=2, blank=True, null=True)
    fecha_mov = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'entrada_salida_acce'
        auto_created = True

class controlinventarioacce(models.Model):
    id = models.AutoField(primary_key=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_cierre = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'controlinventarioacce'
        auto_created = True
   
class espejo_inventarioacce_ant(models.Model):
    id = models.AutoField(primary_key=True)
    id_inventario = models.IntegerField(blank=True, null=True)
    id_item = models.CharField(max_length=50,blank=True, null=True)
    cantidad = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        managed = False
        db_table = 'espejo_inventarioacce_ant'
        auto_created = True
      
class espejo_inventarioacce_desp(models.Model):
    id = models.AutoField(primary_key=True)
    id_inventario = models.IntegerField(blank=True, null=True)
    id_item = models.CharField(max_length=50,blank=True, null=True)
    cantidad = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        managed = False
        db_table = 'espejo_inventarioacce_desp'
        auto_created = True
         

class entrada_accesorios(models.Model):
    id = models.AutoField(primary_key=True)
    id_item = models.CharField(max_length=50,blank=True, null=True) 
    cantidad = models.IntegerField(blank=True, null=True, default=0)
    fecha_entrada = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'entrada_accesorios'
        auto_created = True

class inv_accesorios_temp(models.Model):
    id = models.AutoField(primary_key=True)
    id_item = models.CharField(max_length=50,blank=True, null=True)
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    cantidad = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        managed = False
        db_table = 'inv_accesorios_temp'
        auto_created = True

class rpt_kardex(models.Model):
    id = models.AutoField(primary_key=True)
    id_item = models.CharField(max_length=50,blank=True, null=True)
    descripcion = models.CharField(max_length=250, blank=True, null=True)
    ult_actualizacion = models.IntegerField(blank=True, null=True, default=0)
    entrada_merc = models.IntegerField(blank=True, null=True, default=0)
    salidas = models.IntegerField(blank=True, null=True, default=0)
    entradas = models.IntegerField(blank=True, null=True, default=0)
    existencia_actual = models.IntegerField(blank=True, null=True, default=0)
    dif = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        managed = False
        db_table = 'rpt_kardex'
        auto_created = True


class formulario_pedido(models.Model):
    id = models.AutoField(primary_key=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    Nombre = models.CharField(max_length=200, blank=False, null=False)
    telefono = models.CharField(
        max_length=9,
        validators=[
            RegexValidator(
                regex=r'^\d{9}$',
                message="El número de teléfono debe tener exactamente 9 dígitos.",
                code='invalid_phone_number'
            )
        ],
        null=False,
        blank=False
    )
    fecha_entrega = models.DateField()
    fecha_evento = models.DateField()
    cantidad_radios = models.PositiveIntegerField(null = False, default=0 )
    cantidad_cobras = models.PositiveIntegerField(null = False, default=0)
    cantidad_manos_libres = models.PositiveIntegerField(null = False, default=0)
    cantidad_tipo_escolta = models.PositiveIntegerField(null = False, default=0)
    comentarios = models.TextField (blank = True, null=True)
    direccion_entrega = models.TextField(blank = False, null=False)

    class Meta:
        managed = False
        db_table = 'formulario_pedido'
        auto_created = True