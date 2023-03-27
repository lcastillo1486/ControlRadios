from django.urls import path
from cliente import views

urlpatterns = [
    path('cliente/',views.clientes),
]