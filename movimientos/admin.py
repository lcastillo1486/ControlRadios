from django.contrib import admin
from .models import tipoRadios, invSeriales, estadoRadios, CajasMikrot

# Register your models here.

admin.site.register(tipoRadios)
admin.site.register(invSeriales)
admin.site.register(estadoRadios)
admin.site.register(CajasMikrot)