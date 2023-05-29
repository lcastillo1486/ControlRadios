from django.shortcuts import render, redirect
from django.http import HttpResponse
from ordenes.models import ordenRegistro
from movimientos.models import salidasDetalle
from .forms import radiotipos, agregarInven, formBuscaRadio, guardaEntradaRx, formEntradaDetalle
from django.contrib import messages
from .models import movimientoRadios, invSeriales, entradaDetalle, accesoriosFaltantes, radiosFantantes, vista_radios_faltantes, vista_accesorios_faltantes, vista_movimiento_radios_tipos
from cliente.models import cliente
from django import forms
from django.db import models
from io import BytesIO
import datetime

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, legal, portrait
from reportlab.lib.units import cm
# Create your views here.

def entradaRadios(request, id):

    form = guardaEntradaRx()
    formEntrada = formEntradaDetalle()
    ordenes = ordenRegistro.objects.get(id = id)
    msalida = salidasDetalle.objects.get(id_orden=id)
    radiosCargadas = movimientoRadios.objects.filter(id_salida = id, estado = "D")

    if request.method == 'POST':

        form = guardaEntradaRx(request.POST)
        
        if form.is_valid():
            a = form.cleaned_data['serial']
            ##comprobar que existe una salida con ese serial y ese numero de salida
            if not movimientoRadios.objects.filter(serial = a, id_salida = id, estado = "F").exists():
                return render(request, 'entradas.html',{"listado_entrada": msalida, "listado_orden":ordenes, "listadoRadiosCargadas":radiosCargadas, "form":form, 
                                                        "error": "El serial ingresado no corresponde a la salida", "formEntrada":formEntrada})
            ##valida si ya fue agregado
            if movimientoRadios.objects.filter(serial = a, id_salida = id, estado = "D").exists():
                return render(request, 'entradas.html',{"listado_entrada": msalida, "listado_orden":ordenes, "listadoRadiosCargadas":radiosCargadas, "form":form, 
                                                        "error": "El serial ingresado ya fue agregado", "formEntrada":formEntrada})
            
            else:
                valExisteRxSalida = movimientoRadios.objects.get(serial = a, id_salida = id, estado = "F")
                a = form.save(commit=False)
                a.id_salida = id
                a.estado = 'D'
                a.id_tipo = valExisteRxSalida.id_tipo
                a.save()

                d = a.serial

                #borrar si existe en faltantes

                if radiosFantantes.objects.filter(fserial = d, id_salida = id).exists():
                    borrarrx = radiosFantantes.objects.filter(fserial = d, id_salida = id)
                    borrarrx.delete()


                #cambiar el estatus del radio en el inventario

                cambiaestado =  invSeriales.objects.get(codigo = d)
                cambiaestado.estado_id = 4
                cambiaestado.save()
                


            ordenes = ordenRegistro.objects.get(id = id)
            msalida = salidasDetalle.objects.get(id_orden=id)

            radiosCargadas = movimientoRadios.objects.filter(id_salida = id, estado = "D")
            return render(request, 'entradas.html',{"listado_entrada": msalida, "listado_orden":ordenes, "listadoRadiosCargadas":radiosCargadas, "form":form, 
                                                    "formEntrada":formEntrada})

def entradas(request, id):

    form = guardaEntradaRx()
    formEntrada = formEntradaDetalle()
    context = {'form':form}

    ordenes = ordenRegistro.objects.get(id = id)
    msalida = salidasDetalle.objects.get(id_orden=id)

#buscar las radios cargadas

    radiosCargadas = movimientoRadios.objects.filter(id_salida = id, estado = "D")
    return render(request, 'entradas.html',{"listado_entrada": msalida, "listado_orden":ordenes, "listadoRadiosCargadas":radiosCargadas, "form":form, 
                                             "formEntrada":formEntrada})

def salidas(request):
    ordenes = ordenRegistro.objects.filter(estado_id = 2)
    return render(request, 'salidas.html', {"listaOrdenes": ordenes})

def ordenesProcesadas(request):
    ordenes = ordenRegistro.objects.filter(estado_id = 5)
    return render(request, 'ordenesProcesadas.html', {"listaOrdenes": ordenes})

def ordenesCerradas(request):
    ordenes = ordenRegistro.objects.filter(estado_id = 3)
    return render(request, 'ordenesCerradas.html', {"listaOrdenes": ordenes})

def ordenesDevueltas(request):
    
    devueltas = entradaDetalle.objects.all()

    return render(request, 'ordenesDevueltas.html', {"listaOrdenes": devueltas})

def ordenDetalle(request, id):
    detalle = ordenRegistro.objects.get(id=id)
    return render(request, 'editarOrden.html', {"listaDetalles": detalle})

def detalleOrdenCerrada(request, id):
    detalle = ordenRegistro.objects.get(id=id)
    return render(request, 'editarOrden.html', {"listaDetalles": detalle})

def generarSalida(request, id):
    
    try:
        detalle_salida = ordenRegistro.objects.get(id=id)
        cuenta_radios = movimientoRadios.objects.filter(id_salida = id).count()
        msalida = salidasDetalle.objects.get(id_orden=id)
        form = radiotipos()
        context = {'formRadios': form}
        return render(request, 'salidaGenerada.html', {"salidaGenerada": msalida, "datosOrden": detalle_salida, 'formRadios': form, "cantidad_radios":cuenta_radios})

    except:
        gsalidas = salidasDetalle(id_orden=id, cobras=detalle_salida.cantidad_cobras, cargadores=detalle_salida.cantidad_cargadores,
                              handsfree=detalle_salida.cantidad_manos_libres, cascos=detalle_salida.cantidad_cascos, repetidoras=detalle_salida.cantidad_repetidoras,
                              estaciones=detalle_salida.cantidad_estaciones, baterias = detalle_salida.cantidad_baterias)
        gsalidas.save()
        # detalle_salida = ordenRegistro.objects.get(id=id)
        # b = detalle_salida
        # b.estado_id = 5
        # b.save() 
        form = radiotipos()
        context = {'formRadios': form}
        msalida = salidasDetalle.objects.get(id_orden=id)
        return render(request, 'salidaGenerada.html', {"salidaGenerada": msalida, "datosOrden": detalle_salida, 'formRadios': form})

def guardarDetalleRadio(request, id, id_orden):

    form = radiotipos()
    context = {'form':form}

    detalle_salida = ordenRegistro.objects.get(id = id_orden)
    cuenta_radios = movimientoRadios.objects.filter(id_salida = id).count()
    msalida = salidasDetalle.objects.get(id_orden = id_orden)
    serial_radios = movimientoRadios.objects.filter(id_salida = id)    
        
    if request.method == 'POST':
            
            form = radiotipos(request.POST)
            if form.is_valid():
##valida que exista 
                a = form.cleaned_data['serial']
                valida_serial = invSeriales.objects.filter(codigo = a).count()

                if valida_serial == 0:
                    return render(request, 'salidaGenerada.html', {"salidaGenerada": msalida,"formRadios": form, "datosOrden": detalle_salida, "cantidad_radios":cuenta_radios, 
                'error':'El serial que intenta agregar a la salida, no existe'})

##valida si la cantidad ingresada corresponde a la orden
##aqui debe llevar a otra vista que sea la salida
                if cuenta_radios >= detalle_salida.cantidad_radios: 
                     return render(request,'salidaDefinitiva.html', {"salidaGenerada": msalida, "datosOrden": detalle_salida, "cantidad_radios":cuenta_radios,"serial_radios":serial_radios})

##validar que ya no exista en la salida
                b = form.cleaned_data['serial']
                valida_serial_salida = movimientoRadios.objects.filter(serial = b, id_salida = id).count()

                if  valida_serial_salida == 1:
                        return render(request, 'salidaGenerada.html', {"salidaGenerada": msalida,"formRadios": form, "datosOrden": detalle_salida, "cantidad_radios":cuenta_radios, 
                        'error':'Este serial ya existe en la orden'})

##validar el estado del radio
                #d = form.cleaned_data['serial']
                valida_estado = invSeriales.objects.get(codigo = a)

                if valida_estado.estado_id != 4:
                    return render(request, 'salidaGenerada.html', {"salidaGenerada": msalida,"formRadios": form, "datosOrden": detalle_salida, "cantidad_radios":cuenta_radios, 
                'error':'El serial que intenta agregar no esta disponible'})

                else:

                    a = form.save(commit=False)
                    a.id_salida = id
                    a.estado = 'F'
                    a.save()

##cambia el estado del radio despues de guardarlo para que no este disponible
                    c = form.cleaned_data['serial']
                    cambiaestado =  invSeriales.objects.get(codigo = c)
                    cambiaestado.estado_id = 5
                    cambiaestado.save()

                    detalle_salida = ordenRegistro.objects.get(id=id_orden)        
                    cuenta_radios = movimientoRadios.objects.filter(id_salida = id).count()
                    serial_radios = movimientoRadios.objects.filter(id_salida = id)
                    msalida = salidasDetalle.objects.get(id_orden=id_orden)

#aqui deberia generar el ticket e imprimir otra vista 
#                   # cambia el estado de la orden automaticamente al completar la cantidad de radios
                    if cuenta_radios == detalle_salida.cantidad_radios:
                        ##cierra la orden
                        detalle_salida = ordenRegistro.objects.get(id=id_orden)
                        e = detalle_salida
                        e.estado_id = 5
                        e.save() 
                        return redirect('ordenesProcesadas')
                    
                    return render(request, 'salidaGenerada.html', {"salidaGenerada": msalida, "datosOrden": detalle_salida, "formRadios": form, "cantidad_radios":cuenta_radios,"serial_radios":serial_radios})
                    
    else:
        return render(request, 'salidaGenerada.html', {"salidaGenerada": msalida, "datosOrden": detalle_salida, "formRadios": form, "cantidad_radios":cuenta_radios,"serial_radios":serial_radios})
            
def inventario(request):

    inv_disp = invSeriales.objects.filter(estado_id =4)
    cuenta_disponibles = invSeriales.objects.filter(estado_id =4).count()
    inv_nodisp = invSeriales.objects.filter(estado_id =5)
    cuenta_nodisponibles = invSeriales.objects.filter(estado_id =5).count()
    inv_malogrado = invSeriales.objects.filter(estado_id =6)
    cuenta_malogrado = invSeriales.objects.filter(estado_id =6).count()

    form = agregarInven()
    context = {'form':form}

    if request.method == 'POST':
        form = agregarInven(request.POST)
        
        if form.is_valid():
            b = form.cleaned_data['codigo']
            if invSeriales.objects.filter(codigo =b).exists():
                return render(request, 'inventario.html', {"form": form,"listaDisponibles":inv_disp, "listaNoDisponible":inv_nodisp, "listaMalogrado":inv_malogrado, "cantidadDisponible":cuenta_disponibles,
                "cantidadnoDispo":cuenta_nodisponibles,"cantidadMalogrado":cuenta_malogrado, "buscaradios":formBuscaRadio})
            else:           
                form.save() 
                return render(request,'inventario.html', {"form": form,"listaDisponibles":inv_disp, "listaNoDisponible":inv_nodisp, "listaMalogrado":inv_malogrado, "cantidadDisponible":cuenta_disponibles,
                "cantidadnoDispo":cuenta_nodisponibles, "cantidadMalogrado":cuenta_malogrado, "buscaradios":formBuscaRadio})         

    return render(request,'inventario.html', {"form": form,"listaDisponibles":inv_disp, "listaNoDisponible":inv_nodisp, "listaMalogrado":inv_malogrado, "cantidadDisponible":cuenta_disponibles,
    "cantidadnoDispo":cuenta_nodisponibles,"cantidadMalogrado":cuenta_malogrado,"buscaradios":formBuscaRadio})

def movimientosRadios(request):


    inv_disp = invSeriales.objects.filter(estado_id =4)
    cuenta_disponibles = invSeriales.objects.filter(estado_id =4).count()
    inv_nodisp = invSeriales.objects.filter(estado_id =5)
    cuenta_nodisponibles = invSeriales.objects.filter(estado_id =5).count()
    inv_malogrado = invSeriales.objects.filter(estado_id =6)
    cuenta_malogrado = invSeriales.objects.filter(estado_id =6).count()

    form = agregarInven()
    context = {'form':form}

    formBuscarx = formBuscaRadio()

    if request.method == 'POST':

        serial = request.POST['serial']
        valida_serial = invSeriales.objects.filter(codigo = serial).count()
        if valida_serial == 0:
            return render(request, 'inventario.html', {"form": form,"listaDisponibles":inv_disp, "listaNoDisponible":inv_nodisp, "listaMalogrado":inv_malogrado, "cantidadDisponible":cuenta_disponibles,
                "cantidadnoDispo":cuenta_nodisponibles,"cantidadMalogrado":cuenta_malogrado, "buscaradios":formBuscaRadio, 'error01':'el serial no existe'})
        else:
            estadorx = invSeriales.objects.get(codigo = serial)
            ultima_salida = movimientoRadios.objects.filter(serial = serial)
            ultima_fecha = ultima_salida.aggregate(fecha_maxima=models.Max('fecha_creacion'))['fecha_maxima']
            if ultima_fecha is not None:
                formatedDate = ultima_fecha.strftime("%d/%m/%Y %H:%M:%S")

                ultimo_cliente = movimientoRadios.objects.get(fecha_creacion = ultima_fecha, serial = serial)
                salida_id = ultimo_cliente.id_salida

                detalle_id = salidasDetalle.objects.get(id = salida_id)
                
                numero_orden = detalle_id.id_orden
                #verifica aqui
                orden_cliente = ordenRegistro.objects.get(id = numero_orden)
                nombre_cliente = orden_cliente.cliente
                
            else:
                formatedDate = 'aun no tiene salidas'
                nombre_cliente = 'aun no tiene salidas'

        return render(request, 'inventario.html', {"form": form,"listaDisponibles":inv_disp, "listaNoDisponible":inv_nodisp, "listaMalogrado":inv_malogrado, "cantidadDisponible":cuenta_disponibles,
                "cantidadnoDispo":cuenta_nodisponibles,"cantidadMalogrado":cuenta_malogrado, "estado":estadorx.estado,"buscaradios":formBuscaRadio, "ultima_salida":formatedDate, "cliente":nombre_cliente})

def cambiaEstadoEntregado(request, id):
    detalle_salida = ordenRegistro.objects.get(id=id)
    b = detalle_salida
    b.estado_id = 3
    b.save() 

    ordenes = ordenRegistro.objects.filter(estado_id = 3)
    return render(request, 'ordenesCerradas.html', {"listaOrdenes": ordenes})

def generarPDFPreparados(request, id):

    ordenes = ordenRegistro.objects.get(id = id)
    b = ordenes

    cliente = str(b.cliente)
    radios = str(b.cantidad_radios)
    cobras = str(b.cantidad_cobras)
    baterias = str(b.cantidad_baterias)
    cargadores = str(b.cantidad_cargadores)
    manos_libres = str(b.cantidad_manos_libres)
    cascos = str(b.cantidad_cascos)
    repetidoras = str(b.cantidad_repetidoras)
    estaciones = str(b.cantidad_estaciones)
    fentrega = str(b.fecha_entrega)
    pedido = str(b.id)

    buffer = BytesIO()
    tamano_pagina =  (20*cm, 10*cm)
    pdf = canvas.Canvas(buffer, pagesize=tamano_pagina)
   

    pdf.drawString(2*cm, 9*cm,"N° Pedido: "+ pedido)
    pdf.drawString(2*cm, 8*cm, "Cliente: "+ cliente)
    pdf.drawString(2*cm, 7*cm,"Fecha entrega: " +fentrega)
    if b.cantidad_radios > 0:
        pdf.drawString(2*cm, 6*cm, "Radios: "+ radios)
    if b.cantidad_cobras > 0:
        pdf.drawString(2*cm, 5.5*cm, "Cobras: "+ cobras)
    if b.cantidad_baterias > 0:
        pdf.drawString(2*cm, 5*cm, "Baterias extra: "+ baterias)
    if b.cantidad_cargadores > 0:
        pdf.drawString(2*cm, 4.5*cm, "Cargadores: " + cargadores)
    if b.cantidad_manos_libres > 0:
        pdf.drawString(2*cm, 4*cm,"Manos libres: " + manos_libres)
    if b.cantidad_cascos > 0:
        pdf.drawString(2*cm, 3.5*cm,"Cascos: " + cascos)
    if b.cantidad_repetidoras > 0:
        pdf.drawString(2*cm, 3*cm,"Repetidoras: " + repetidoras)
    if b.cantidad_estaciones > 0:
        pdf.drawString(2*cm, 2.5*cm,"Estaciones: " + estaciones)
    
    
    pdf.showPage()

    pdf.save()

    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="archivo.pdf"'


    return response

def generarEntrada(request, id):

    if request.method == 'POST':
        formEntrada = formEntradaDetalle(request.POST)

        if formEntrada.is_valid():

            if accesoriosFaltantes.objects.filter(id_salida = id).exists():
                cobras = formEntrada.cleaned_data['cobras']
                baterias = formEntrada.cleaned_data['baterias']
                cargadores = formEntrada.cleaned_data['cargadores']
                handsfree = formEntrada.cleaned_data['handsfree']
                cascos = formEntrada.cleaned_data['cascos']
                repetidoras = formEntrada.cleaned_data['repetidoras']
                estaciones = formEntrada.cleaned_data['estaciones']
                observaciones = formEntrada.cleaned_data['observaciones']

                actualiza_acce = accesoriosFaltantes.objects.get(id_salida = id)
                actualiza_acce.fcobras = actualiza_acce.fcobras - cobras
                actualiza_acce.fbaterias = actualiza_acce.fbaterias - baterias
                actualiza_acce.fcargadores = actualiza_acce.fcargadores - cargadores
                actualiza_acce.fhandsfree = actualiza_acce.fhandsfree - handsfree
                actualiza_acce.fcascos = actualiza_acce.fcascos - cascos
                actualiza_acce.frepetidoras = actualiza_acce.frepetidoras - repetidoras
                actualiza_acce.festaciones = actualiza_acce.festaciones - estaciones
                actualiza_acce.save()

                actualiza_acce = accesoriosFaltantes.objects.get(id_salida = id) 
                if actualiza_acce.fcobras + actualiza_acce.fbaterias + actualiza_acce.fcargadores + actualiza_acce.fhandsfree + actualiza_acce.fcascos + actualiza_acce.frepetidoras + actualiza_acce.festaciones == 0:
                    actualiza_acce.delete()
                    return redirect('/verFaltante/')
                return redirect('/verFaltante/')

            #tomo cantidades enviadas desde form
            cobras = formEntrada.cleaned_data['cobras']
            baterias = formEntrada.cleaned_data['baterias']
            cargadores = formEntrada.cleaned_data['cargadores']
            handsfree = formEntrada.cleaned_data['handsfree']
            cascos = formEntrada.cleaned_data['cascos']
            repetidoras = formEntrada.cleaned_data['repetidoras']
            estaciones = formEntrada.cleaned_data['estaciones']
            observaciones = formEntrada.cleaned_data['observaciones']

            #busca las cantidades en la salida para comparar
            datosSalida = salidasDetalle.objects.get(id = id)
            numeroOrden = datosSalida.id_orden
            cobrasSal = datosSalida.cobras
            bateriasSal = datosSalida.baterias
            cargadoresSal = datosSalida.cargadores
            handsfreeSal = datosSalida.handsfree
            cascosSal = datosSalida.cascos
            repetidorasSal = datosSalida.repetidoras
            estacionesSal = datosSalida.estaciones

            ordenes = ordenRegistro.objects.get(id = id)
            msalida = salidasDetalle.objects.get(id_orden=id)
            radiosCargadas = movimientoRadios.objects.filter(id_salida = id, estado = "D")
            cuentaRxcargadas = movimientoRadios.objects.filter(id_salida = id, estado = "D").count()
            cuentaRxOrden =  movimientoRadios.objects.filter(id_salida = id, estado = "F").count()
            formEntrada = formEntradaDetalle()
            form = guardaEntradaRx()

            #validar las cantidades no deben ser mayores 

            if cobras > cobrasSal :
                return render(request, 'entradas.html',{"listado_entrada": msalida, "listado_orden":ordenes, "listadoRadiosCargadas":radiosCargadas, "form":form, 
                                             "formEntrada":formEntrada, "error1":"La cantidades ingresadas no pueden ser mayores a las registradas en el pedido. Verifique"})            
            if baterias > bateriasSal :
                return render(request, 'entradas.html',{"listado_entrada": msalida, "listado_orden":ordenes, "listadoRadiosCargadas":radiosCargadas, "form":form, 
                                             "formEntrada":formEntrada, "error1":"La cantidades ingresadas no pueden ser mayores a las registradas en el pedido. Verifique"})
            if cargadores > cargadoresSal :
                return render(request, 'entradas.html',{"listado_entrada": msalida, "listado_orden":ordenes, "listadoRadiosCargadas":radiosCargadas, "form":form, 
                                             "formEntrada":formEntrada, "error1":"La cantidades ingresadas no pueden ser mayores a las registradas en el pedido. Verifique"})
            if handsfree > handsfreeSal :
                return render(request, 'entradas.html',{"listado_entrada": msalida, "listado_orden":ordenes, "listadoRadiosCargadas":radiosCargadas, "form":form, 
                                             "formEntrada":formEntrada, "error1":"La cantidades ingresadas no pueden ser mayores a las registradas en el pedido. Verifique"})
            if cascos > cascosSal :
                return render(request, 'entradas.html',{"listado_entrada": msalida, "listado_orden":ordenes, "listadoRadiosCargadas":radiosCargadas, "form":form, 
                                             "formEntrada":formEntrada, "error1":"La cantidades ingresadas no pueden ser mayores a las registradas en el pedido. Verifique"})
            if repetidoras > repetidorasSal :
                return render(request, 'entradas.html',{"listado_entrada": msalida, "listado_orden":ordenes, "listadoRadiosCargadas":radiosCargadas, "form":form, 
                                             "formEntrada":formEntrada, "error1":"La cantidades ingresadas no pueden ser mayores a las registradas en el pedido. Verifique"})
            if estaciones > estacionesSal :
                return render(request, 'entradas.html',{"listado_entrada": msalida, "listado_orden":ordenes, "listadoRadiosCargadas":radiosCargadas, "form":form, 
                                             "formEntrada":formEntrada, "error1":"La cantidades ingresadas no pueden ser mayores a las registradas en el pedido. Verifique"})
            
            # crear el registro de lo faltante (accesorios)

            faltantecobras = cobrasSal - cobras
            faltantebat = bateriasSal - baterias
            faltantecarga = cargadoresSal - cargadores
            faltantehands = handsfreeSal - handsfree
            faltantecascos = cascosSal - cascos
            faltanterep = repetidorasSal - repetidoras
            faltanteest = estacionesSal - estaciones

            sumafaltante = faltantecobras + faltantebat + faltantecarga + faltantehands + faltantecascos + faltanterep + faltanteest

            if sumafaltante > 0:
                guardafaltante = accesoriosFaltantes(id_salida = id, fcobras = faltantecobras, fbaterias = faltantebat, fcargadores = faltantecarga,
                                                     fhandsfree = faltantehands, fcascos = faltantecascos, frepetidoras = faltanterep,
                                                     festaciones = faltanteest)
                
                guardafaltante.save()

            # crear el registro de lo faltante (radios)

            rxOrden = movimientoRadios.objects.filter(id_salida = id, estado = "F")

            for i in rxOrden:
                serfaltante = i.serial

                if not movimientoRadios.objects.filter(serial = serfaltante, id_salida = id, estado = "D").exists():
                    guardafaltanterx = radiosFantantes()
                    guardafaltanterx.id_salida = id
                    guardafaltanterx.fserial = serfaltante
                    guardafaltanterx.save()

            numorden = salidasDetalle.objects.get(id_orden=id)
            numordena = numorden.id_orden
            client = ordenRegistro.objects.get(id=numordena)
            client_id = client.cliente
            client.estado_id = 4
            client.save()
            guardaEntrada = entradaDetalle(id_salida = id, id_orden = numordena, cobras = cobras, baterias = baterias, cargadores = cargadores,
                                           handsfree = handsfree, cascos = cascos, repetidoras = repetidoras, estaciones = estaciones, cliente = client_id,
                                            observaciones = observaciones)
            
            guardaEntrada.save()

            return redirect('/ordenesCerradas/')

def verFaltante(request):
    
    rx_listado_faltante = vista_radios_faltantes.objects.all()
    listadoFantante = vista_accesorios_faltantes.objects.all()
    return render(request,"faltantes.html",{"listAccFaltante":listadoFantante, "listadorxfaltante":rx_listado_faltante})

def generarPDFGuia(request, id):
    
    detalle_acce = salidasDetalle.objects.get(id_orden = id)
    b = detalle_acce

    orden = b.id_orden

    ordenes = ordenRegistro.objects.get(id = orden)

    c = ordenes

    fecha_actual = datetime.date.today().strftime('%d/%m/%Y')

    radios = movimientoRadios.objects.filter(id_salida = id).values_list('serial', flat=True)

    d = radios

    rx_amarillas = vista_movimiento_radios_tipos.objects.filter(id_salida = id, tipo = 'EP 450 (Amarillas)').count()
    rx_moradas =  vista_movimiento_radios_tipos.objects.filter(id_salida = id, tipo = 'DEP 450 (Moradas)').count()
    rx_plomo = vista_movimiento_radios_tipos.objects.filter(id_salida = id, tipo = 'DEP 450 (Plomo)').count()



    cliente = str(c.cliente)
    cobras = str(b.cobras)
    cargadores = str(b.cargadores)
    handsfree = str(b.handsfree)
    cascos = str(b.cascos)
    estaciones = str(b.estaciones)
    repetidoras = str(b.repetidoras)
    baterias = str(b.baterias)
    fecha_entrega = str(c.fecha_entrega)
    fecha_evento = (c.fecha_evento_desde).strftime('%d/%m/%Y')
    rx = d

    buffer = BytesIO()

    pdf = canvas.Canvas(buffer)
    ancho_pagina, altura_pagina = letter = (21.59*cm, 27.94*cm)

    pdf.drawString(5*cm, altura_pagina - 7*cm, str(id))
    pdf.drawString(5*cm, altura_pagina - 9.35*cm, str(cliente))
    pdf.drawString(15.5*cm, altura_pagina - 9.35*cm, str(fecha_actual))
    pdf.drawString(15.5*cm, altura_pagina - 10*cm, 'Evento: '+ str(fecha_evento))
    if b.cobras > 0:
        pdf.drawString(14*cm, altura_pagina - 15.15*cm, str(cobras) + ' UND')
    if b.handsfree > 0:
        pdf.drawString(14*cm, altura_pagina - 16.65*cm, str(handsfree) + ' UND')
    if b.cascos > 0:
        pdf.drawString(5*cm, altura_pagina - 17.45*cm, str('Headset Antiruido'))
        pdf.drawString(14*cm, altura_pagina - 17.45*cm, str(cascos + ' UND'))
    if b.baterias > 0:
        pdf.drawString(14*cm, altura_pagina - 19.25*cm, str(baterias) + ' UND')
    if b.cargadores > 0:
        pdf.drawString(14*cm, altura_pagina - 20.25*cm, str(cargadores + ' UND'))
    #if b.estaciones >0:
        #pdf.drawString(14*cm, altura_pagina - 12*cm, str(estaciones + ' UND'))
    if b.repetidoras > 0:
        pdf.drawString(5*cm, altura_pagina - 20.85*cm, str('Repetidoras'))
        pdf.drawString(14*cm, altura_pagina - 20.85*cm, str(repetidoras + ' UND'))
    #radios
    if rx_amarillas > 0:
        pdf.drawString(14*cm, altura_pagina - 11.95*cm, str(rx_amarillas))
    if rx_moradas > 0:
        pdf.drawString(14*cm, altura_pagina - 13.45*cm, str(rx_moradas))
    if rx_plomo > 0:
        pdf.drawString(14*cm, altura_pagina - 12.65*cm, str(rx_plomo))
    # #y = 110
    x = 60
    for i in rx:
        pdf.drawString(x, 110, str(i))
        #y += 20
        x += 50
    
    

    pdf.showPage()

    pdf.save()

    buffer.seek(0)

    nombre_archivo = str(id)+'_'+str(fecha_entrega)+'.pdf'
   
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename= {nombre_archivo}'


    return response




    

    






        
      
        

    

 
    




    
