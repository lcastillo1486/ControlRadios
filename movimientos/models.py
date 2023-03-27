from django.db import models
from ordenes.models import ordenRegistro, cliente

# Create your models here.

class salidasDetalle(models.Model):
    id_orden = models.PositiveIntegerField(null=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
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
    fecha_creacion = models.DateTimeField(auto_now_add=True)

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
    fecha_creacion = models.DateTimeField(auto_now_add=True)
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






    



