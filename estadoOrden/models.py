from django.db import models

# Create your models here.
class estado(models.Model):
    descripcion = models.CharField(max_length=20)

    def __str__(self):
        return str(self.descripcion)
