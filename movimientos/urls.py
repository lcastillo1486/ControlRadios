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
    path('informe/',views.generaInformes),
    path('informePdfTotales/',views.generarPDFtotales),
    path('entradatotal/<int:id>/<int:id_orden>',views.entradatotal),
    path('auditoria/',views.auditoria),
    path('anularorden/<int:id>',views.anularorden),
    path('listadocxc/',views.listadocxc),
    path('listadocxcfacturado/',views.listadocxcfacturado),
    path('subirpdf/<int:id>/<int:id_salida>',views.subir_factura_pdf),
    path('subirpdfnosunat/<int:id>/<int:id_salida>',views.subir_factura_pdf_no_sunat),
    path('descargarfacturapdf/<int:id>',views.ver_factura_pdf),
    path('formregistrafactura/<int:id>/<str:cliente>/<str:ruc>/<str:id_salida>/<str:razon_social>',views.form_registra_fact),
    path('formregistrafacturanosunat/<int:id>/<str:cliente>/<str:ruc>/<str:id_salida>/<str:razon_social>',views.form_registra_fact_no_sunat),
    path('revertirfactura/<int:id>',views.revertir_factura),
    path('formregistrarpago/<int:id>/<str:cliente>/<str:ruc>/<str:id_salida>/<str:razon_social>',views.form_registrar_pago),
    path('registrarpago/<int:id>/<int:id_salida>',views.registrar_pago),
    path('listadopagado/',views.listadocxcpagado),
    path('descargarcomprobante/<int:id>',views.ver_comprobante_pago),
    path('reportescxc/',views.reportescxc),
    path('buscarlistadocxc/',views.buscarlistadocxccliente),
    path('buscarlistadocxcruc/',views.buscarlistadocxcruc),
    path('buscarlistadocxcsalida/',views.buscarlistadocxcidsalida),
    path('buscarlistadocxcorden/',views.buscarlistadocxcidorden),
    path('buscarlistadofacturadocxc/',views.buscarlistadofacturadocliente),
    path('buscarlistadofacturadoruc/',views.buscarlistadofacturadoruc),
    path('buscarlistadofacturadosalida/',views.buscarlistadofacturadoidsalida),
    path('buscarlistadofacturadoorden/',views.buscarlistadofacturadoidorden),
    path('buscarlistadocobradocxc/',views.buscarlistadocobradocliente),
    path('buscarlistadocobradoruc/',views.buscarlistadocobradoruc),
    path('buscarlistadocobradosalida/',views.buscarlistadocobradoidsalida),
    path('buscarlistadocobradoreferencia/',views.buscarlistadocobradoreferencia),
    path('generaPDFdetallecobrar/<str:cliente>',views.pdfporcobrar_detalle),
    path('listadocxcfacturadoabono/',views.listadocxcfacturadoAbono),
    path('detalleabonos/<int:id>',views.detalleabonado),
    path('descargarcomprobanteabono/<int:id>',views.ver_comprobante_pago_abono),
    path('borrarabono/<int:id>',views.revertir_abono),
    path('controlrxevento/<int:id>',views.controlrxevento, name='controlrxevento'),
    path('cargarrxevento/<int:id>',views.cargarxordenevento, name='cargarx'),
    path('controlrxeventorecojo/<int:id>',views.controlrxeventorecojo, name='controlrxeventorecojo'),
    path('imprimir/<int:id>', views.print_view, name='print_template'),
    path('eliminarserial/<int:id>', views.eliminar_serial, name='eliminar_serial'),
    path('mikrotik/<str:ip>', views.mikrotik),
    path('dash/', views.cargadash, name='dash'),





]

##recibir parametro 