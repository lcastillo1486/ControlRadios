from django.urls import path
from movimientos import views

urlpatterns = [
    path('entradas/<int:id>',views.entradas),
    path('salidas/',views.salidas),
    path('detalleOrden/<int:id>',views.ordenDetalle),
    path('generarsalida/<int:id>',views.generarSalida),
    path('detalleradios/<int:id>/<int:id_orden>',views.guardarDetalleRadio),
    path('inventario/',views.inventario),
    path('ubicarRadios/',views.movimientosRadios),
    path('ordenesProcesadas/',views.ordenesProcesadas, name="ordenesProcesadas"),
    path('ordenesCerradas/',views.ordenesCerradas),
    path('ordenesDevueltas/',views.ordenesDevueltas),
    path('detalleOrdenCerrada/<int:id>',views.detalleOrdenCerrada),
    path('cambiaEstadoEnt/<int:id>',views.cambiaEstadoEntregado),
    path('generarPDF/<int:id>',views.generarPDFPreparados),
    path('entradaRadios/<int:id>/<int:orden_id>',views.entradaRadios),
    path('generarEntrada/<int:id>/<int:orden_id>',views.generarEntrada),
    path('verFaltante/',views.verFaltante),
    path('generaPDFGuia/<int:id>',views.generarPDFGuia),
    path('guardamochila/<int:id>',views.guardarcolormochila),
    path('guiadevueltos/<int:id>',views.pdfguiadevueltos),
    path('buscaOrdenesDevueltas/',views.buscaOrdenesDevueltas),
    path('monitor/',views.monitor),
    path('generaPDFprint/<int:id>',views.generarPDFprint),




]

##recibir parametro 