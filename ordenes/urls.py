from django.urls import path
from ordenes import views

urlpatterns = [
    path('ordenes/',views.ordenes),
    path('editarOrden/<int:id_orden>', views.buscaEdit),
    path('editarOrdenfactura/<int:id_orden>', views.buscaEditFactura),
    path('buscarcliente/', views.buscar_proveedor)

]