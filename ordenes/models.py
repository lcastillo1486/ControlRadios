from django.db import models
from cliente.models import cliente, razonSocial
from estadoOrden.models import estado
from django.contrib.auth.models import User

# Create your models here.

class orden(models.Model):
    cliente = models.ForeignKey(cliente, on_delete = models.DO_NOTHING)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateField()
    fecha_evento = models.DateField()
    fecha_retiro = models.DateField()
    cantidad_radios = models.PositiveIntegerField(null = True, blank = True )
    cantidad_cobras = models.PositiveIntegerField(null = True, blank = True)
    cantidad_baterias = models.PositiveIntegerField(null = True, blank = True)
    cantidad_cargadores = models.PositiveIntegerField(null = True, blank = True)
    cantidad_manos_libres = models.PositiveIntegerField(null = True, blank = True)
    cantidad_cascos = models.PositiveIntegerField(null = True, blank = True)
    cantidad_repetidoras = models.PositiveIntegerField(null = True, blank = True)
    cantidad_estaciones = models.PositiveIntegerField(null = True, blank = True)
    observaciones = models.TextField (blank = True)
    direccion_entrega = models.TextField(blank = True)
    estado = models.ForeignKey(estado, on_delete=models.DO_NOTHING)


    def __str__(self):
        return str(self.id) + '  -  ' + str(self.cliente)


class ordenRegistro(models.Model):
    cliente = models.ForeignKey(cliente, on_delete = models.DO_NOTHING)
    razon_Social = models.ForeignKey(razonSocial, on_delete=  models.DO_NOTHING, null=True, blank= True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateField()
    fecha_evento_desde = models.DateField()
    fecha_evento_hasta = models.DateField(null=True, blank=True)
    fecha_retiro = models.DateField()
    cantidad_radios = models.PositiveIntegerField(null = False, default=0 )
    cantidad_cobras = models.PositiveIntegerField(null = False, default=0)
    cantidad_baterias = models.PositiveIntegerField(null = False, default=0)
    cantidad_cargadores = models.PositiveIntegerField(null = False, default=0)
    cantidad_manos_libres = models.PositiveIntegerField(null = False, default=0)
    cantidad_cascos = models.PositiveIntegerField(null = False, default=0)
    cantidad_repetidoras = models.PositiveIntegerField(null = False, default=0)
    cantidad_estaciones = models.PositiveIntegerField(null = False, default=0)
    observaciones = models.TextField (blank = True)
    direccion_entrega = models.TextField(blank = True)
    estado = models.ForeignKey(estado, on_delete=models.DO_NOTHING)


    def __str__(self):
        return str(self.id) + '  -  ' + str(self.cliente)


    
    


