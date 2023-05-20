from django.db import models

# Create your models here.
class cliente(models.Model):
    
    ruc = models.CharField(max_length=11, null= True, blank= True)
    nombre = models.CharField(max_length=100)
    direccion = models.TextField(blank=True, null= True)
    email = models.EmailField(blank=True, null= True)
    telefono = models.PositiveBigIntegerField(max_length=9,blank=True, null = True)
    persona_contacto = models.CharField(max_length = 20, null = True, blank = True)

    def __str__(self) -> str:
        return self.nombre

class razonSocial(models.Model):
    denominacion = models.CharField(max_length=50)
    ruc = models.CharField(max_length=11, null= True, blank= True)
    direccion = models.TextField(blank=True, null= True)
    email = models.EmailField(blank=True, null=True)
    telefono = models.PositiveBigIntegerField(max_length=9,blank=True, null = True)
    persona_contacto = models.CharField(max_length = 20, null = True, blank = True)

    def __str__(self) -> str:
        return self.denominacion 
