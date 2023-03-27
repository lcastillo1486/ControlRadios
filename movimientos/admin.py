from django.contrib import admin
from .models import tipoRadios, invSeriales, estadoRadios

# Register your models here.

admin.site.register(tipoRadios)
admin.site.register(invSeriales)
admin.site.register(estadoRadios)