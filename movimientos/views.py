from django.shortcuts import render, redirect
from django.http import HttpResponse
from ordenes.models import ordenRegistro
from movimientos.models import salidasDetalle
from .forms import radiotipos, agregarInven, formBuscaRadio, guardaEntradaRx, formEntradaDetalle
from django.contrib import messages
from .models import movimientoRadios, invSeriales, entradaDetalle, accesoriosFaltantes, radiosFantantes, vista_radios_faltantes, vista_accesorios_faltantes, vista_movimiento_radios_tipos, auditoria, mochila
from cliente.models import cliente
from django import forms
from django.db import models
from io import BytesIO
import datetime
from django.utils import timezone

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, legal, portrait
from reportlab.lib.units import cm
import os


# Create your views here.

def entradaRadios(request, id, orden_id):

    form = guardaEntradaRx()
    formEntrada = formEntradaDetalle()
    ordenes = ordenRegistro.objects.get(id = orden_id)
    msalida = salidasDetalle.objects.get(id_orden=orden_id)
    #verificar aqui el id
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
            # if movimientoRadios.objects.filter(serial = a, id_salida = id, estado = "D").exists():
            #     return render(request, 'entradas.html',{"listado_entrada": msalida, "listado_orden":ordenes, "listadoRadiosCargadas":radiosCargadas, "form":form, 
            #                                             "error": "El serial ingresado ya fue agregado", "formEntrada":formEntrada})
            
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
                


            ordenes = ordenRegistro.objects.get(id = orden_id)
            msalida = salidasDetalle.objects.get(id_orden=orden_id)

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
    color = ""
    if mochila.objects.filter(numero_orden=id).exists():
        mochila_guardada = mochila.objects.get(numero_orden=id)
        color = mochila_guardada.color
    return render(request, 'editarOrden.html', {"listaDetalles": detalle, "mochilaguardada":color})

def detalleOrdenCerrada(request, id):
    detalle = ordenRegistro.objects.get(id=id)
    return render(request, 'editarOrden.html', {"listaDetalles": detalle})

def generarSalida(request, id):
    
    try:
        detalle_salida = ordenRegistro.objects.get(id=id)
        msalida = salidasDetalle.objects.get(id_orden=id)
        salida_id = msalida.id
        if movimientoRadios.objects.filter(id_salida = salida_id).exists():
            cuenta_radios = movimientoRadios.objects.filter(id_salida = salida_id).count()
            serial_radios = movimientoRadios.objects.filter(id_salida = salida_id)
            form = radiotipos()
            context = {'formRadios': form}
            return render(request, 'salidaGenerada.html', {"salidaGenerada": msalida, "datosOrden": detalle_salida, 'formRadios': form, "cantidad_radios":cuenta_radios, "serial_radios":serial_radios})
        else:
            form = radiotipos()
            context = {'formRadios': form}
            return render(request, 'salidaGenerada.html', {"salidaGenerada": msalida, "datosOrden": detalle_salida, 'formRadios': form})
    except:
        gsalidas = salidasDetalle(id_orden=id, cobras=detalle_salida.cantidad_cobras, cargadores=detalle_salida.cantidad_cargadores,
                              handsfree=detalle_salida.cantidad_manos_libres, cascos=detalle_salida.cantidad_cascos, repetidoras=detalle_salida.cantidad_repetidoras,
                              estaciones=detalle_salida.cantidad_estaciones, baterias = detalle_salida.cantidad_baterias)
        gsalidas.save()
#####AUDITORIA############
        ultimo_id = salidasDetalle.objects.latest('id').id
        numero_orden = id
        #capturar usuario actual
        user_nombre = request.user.username
        #fecha y hora actual
        fecha_hora_peru = timezone.localtime(timezone.now())
        fecha_hora_formateada = fecha_hora_peru.strftime('%Y-%m-%d %H:%M:%S')

        log = auditoria(fecha = fecha_hora_formateada, accion = f'Genera Salida N° {ultimo_id} para la orden {numero_orden}', usuario = user_nombre)
        log.save()

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
                    return render(request, 'salidaGenerada.html', {"salidaGenerada": msalida,"formRadios": form, "datosOrden": detalle_salida, "cantidad_radios":cuenta_radios, "serial_radios":serial_radios, 
                'error':'El serial que intenta agregar a la salida, no existe'})

##valida si la cantidad ingresada corresponde a la orden
##aqui debe llevar a otra vista que sea la salida
                if cuenta_radios >= detalle_salida.cantidad_radios: 
                     return render(request,'salidaDefinitiva.html', {"salidaGenerada": msalida, "datosOrden": detalle_salida, "cantidad_radios":cuenta_radios,"serial_radios":serial_radios})

##validar que ya no exista en la salida
                b = form.cleaned_data['serial']
                valida_serial_salida = movimientoRadios.objects.filter(serial = b, id_salida = id).count()

                if  valida_serial_salida == 1:
                        return render(request, 'salidaGenerada.html', {"salidaGenerada": msalida,"formRadios": form, "datosOrden": detalle_salida, "cantidad_radios":cuenta_radios, "serial_radios":serial_radios,
                        'error':'Este serial ya existe en la orden'})

##validar el estado del radio
                #d = form.cleaned_data['serial']
                valida_estado = invSeriales.objects.get(codigo = a)

                if valida_estado.estado_id != 4:
                    return render(request, 'salidaGenerada.html', {"salidaGenerada": msalida,"formRadios": form, "datosOrden": detalle_salida, "cantidad_radios":cuenta_radios, "serial_radios":serial_radios,
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
    amarillas_disp = invSeriales.objects.filter(estado_id =4, tipo_id = 1).count()
    moradas_disp = invSeriales.objects.filter(estado_id =4, tipo_id = 2).count()
    plomo_disp = invSeriales.objects.filter(estado_id =4, tipo_id = 3).count()


    form = agregarInven()
    context = {'form':form}

    if request.method == 'POST':
        form = agregarInven(request.POST)
        
        if form.is_valid():
            b = form.cleaned_data['codigo']
            if invSeriales.objects.filter(codigo =b).exists():
                return render(request, 'inventario.html', {"form": form,"listaDisponibles":inv_disp, "listaNoDisponible":inv_nodisp, "listaMalogrado":inv_malogrado, "cantidadDisponible":cuenta_disponibles,
                "cantidadnoDispo":cuenta_nodisponibles,"cantidadMalogrado":cuenta_malogrado, "buscaradios":formBuscaRadio, "amarillasDisponibles":amarillas_disp, 
                "moradasDisponibles":moradas_disp, "plomoDisponibles":plomo_disp})
            else:           
                form.save() 
                return render(request,'inventario.html', {"form": form,"listaDisponibles":inv_disp, "listaNoDisponible":inv_nodisp, "listaMalogrado":inv_malogrado, "cantidadDisponible":cuenta_disponibles,
                "cantidadnoDispo":cuenta_nodisponibles, "cantidadMalogrado":cuenta_malogrado, "buscaradios":formBuscaRadio, "amarillasDisponibles":amarillas_disp, 
                "moradasDisponibles":moradas_disp, "plomoDisponibles":plomo_disp})         

    return render(request,'inventario.html', {"form": form,"listaDisponibles":inv_disp, "listaNoDisponible":inv_nodisp, "listaMalogrado":inv_malogrado, "cantidadDisponible":cuenta_disponibles,
    "cantidadnoDispo":cuenta_nodisponibles,"cantidadMalogrado":cuenta_malogrado,"buscaradios":formBuscaRadio, "amarillasDisponibles":amarillas_disp, 
    "moradasDisponibles":moradas_disp, "plomoDisponibles":plomo_disp})

def movimientosRadios(request):


    inv_disp = invSeriales.objects.filter(estado_id =4)
    cuenta_disponibles = invSeriales.objects.filter(estado_id =4).count()
    inv_nodisp = invSeriales.objects.filter(estado_id =5)
    cuenta_nodisponibles = invSeriales.objects.filter(estado_id =5).count()
    inv_malogrado = invSeriales.objects.filter(estado_id =6)
    cuenta_malogrado = invSeriales.objects.filter(estado_id =6).count()
    amarillas_disp = invSeriales.objects.filter(estado_id =4, tipo_id = 1).count()
    moradas_disp = invSeriales.objects.filter(estado_id =4, tipo_id = 2).count()
    plomo_disp = invSeriales.objects.filter(estado_id =4, tipo_id = 3).count()

    form = agregarInven()
    context = {'form':form}

    formBuscarx = formBuscaRadio()

    if request.method == 'POST':

        serial = request.POST['serial']
        valida_serial = invSeriales.objects.filter(codigo = serial).count()
        if valida_serial == 0:
            return render(request, 'inventario.html', {"form": form,"listaDisponibles":inv_disp, "listaNoDisponible":inv_nodisp, "listaMalogrado":inv_malogrado, "cantidadDisponible":cuenta_disponibles,
                "cantidadnoDispo":cuenta_nodisponibles,"cantidadMalogrado":cuenta_malogrado,"amarillasDisponibles":amarillas_disp, 
                "moradasDisponibles":moradas_disp, "plomoDisponibles":plomo_disp, "buscaradios":formBuscaRadio, 'error01':'el serial no existe'})
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
                "cantidadnoDispo":cuenta_nodisponibles,"cantidadMalogrado":cuenta_malogrado,"amarillasDisponibles":amarillas_disp, "moradasDisponibles":moradas_disp, "plomoDisponibles":plomo_disp, "estado":estadorx.estado,"buscaradios":formBuscaRadio, "ultima_salida":formatedDate, "cliente":nombre_cliente})

def cambiaEstadoEntregado(request, id):
    detalle_salida = ordenRegistro.objects.get(id=id)
    b = detalle_salida
    b.estado_id = 3
    b.save() 

    #####AUDITORIA############
    numero_orden = id
    #capturar usuario actual
    user_nombre = request.user.username
    #fecha y hora actual
    fecha_hora_peru = timezone.localtime(timezone.now())
    fecha_hora_formateada = fecha_hora_peru.strftime('%Y-%m-%d %H:%M:%S')

    log = auditoria(fecha = fecha_hora_formateada, accion = f'Cambia estado a ENTREGADO a la orden N° {numero_orden}', usuario = user_nombre)
    log.save()



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
    nombre_archivo = str(id)+'_'+str(cliente)+'.pdf'
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename= {nombre_archivo}'


    return response

def generarEntrada(request, id, orden_id):

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

            ordenes = ordenRegistro.objects.get(id = orden_id)
            msalida = salidasDetalle.objects.get(id_orden=orden_id)
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

            numorden = salidasDetalle.objects.get(id_orden=orden_id)
            numordena = numorden.id_orden
            client = ordenRegistro.objects.get(id=numordena)
            client_id = client.cliente
            client.estado_id = 4
            client.save()

            if not entradaDetalle.objects.filter(id_salida = id).exists():
                guardaEntrada = entradaDetalle(id_salida = id, id_orden = numordena, cobras = cobras, baterias = baterias, cargadores = cargadores,
                                           handsfree = handsfree, cascos = cascos, repetidoras = repetidoras, estaciones = estaciones, cliente = client_id,
                                            observaciones = observaciones)
            
                guardaEntrada.save()

                #####AUDITORIA############
                numero_orden = numordena
                #capturar usuario actual
                user_nombre = request.user.username
                #fecha y hora actual
                fecha_hora_peru = timezone.localtime(timezone.now())
                fecha_hora_formateada = fecha_hora_peru.strftime('%Y-%m-%d %H:%M:%S')

                log = auditoria(fecha = fecha_hora_formateada, accion = f'Pedido recibido de salida N° {id} de la orden {numero_orden}', usuario = user_nombre)
                log.save()

            return redirect('/ordenesCerradas/')

def verFaltante(request):
    
    rx_listado_faltante = vista_radios_faltantes.objects.all()
    listadoFantante = vista_accesorios_faltantes.objects.all()
    return render(request,"faltantes.html",{"listAccFaltante":listadoFantante, "listadorxfaltante":rx_listado_faltante})

def generarPDFGuia(request, id):
    
    detalle_acce = salidasDetalle.objects.get(id_orden = id)
    b = detalle_acce

    orden = b.id_orden
    salida_id = b.id

    ordenes = ordenRegistro.objects.get(id = orden)

    c = ordenes

    color_mochila = mochila.objects.get(numero_orden = orden)
    color_descrip = color_mochila.color

    fecha_actual = datetime.date.today().strftime('%d/%m/%Y')

    radios = movimientoRadios.objects.filter(id_salida = salida_id, estado = 'F').values_list('serial', flat=True)

    d = radios

    rx_amarillas = vista_movimiento_radios_tipos.objects.filter(id_salida = salida_id, tipo = 'EP 450 (Amarillas)').count()
    rx_moradas =  vista_movimiento_radios_tipos.objects.filter(id_salida = salida_id, tipo = 'DEP 450 (Moradas)').count()
    rx_plomo = vista_movimiento_radios_tipos.objects.filter(id_salida = salida_id, tipo = 'DEP 450 (Plomo)').count()

    amarillas = rx_amarillas
    moradas = rx_moradas
    plomo = rx_plomo



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
    direccion = str(c.direccion_entrega)
    rx = d

    buffer = BytesIO()

    pdf = canvas.Canvas(buffer)
    ancho_pagina, altura_pagina = letter = (21.59*cm, 27.94*cm)
    tamano_direccion = len(direccion)
    
    if tamano_direccion > 44:
        linea_dir1 = direccion[:44]
        linea_dir2 = direccion[45:88]
        linea_dir3 = direccion[89:133]
    else:
        linea_dir1 = direccion[:44]
        linea_dir2 = ""
        linea_dir3 = "" 

    pdf.drawString(18*cm, altura_pagina - 6.05*cm, str(id))
    pdf.drawString(5*cm, altura_pagina - 9.35*cm, str(cliente))
    pdf.drawString(3.5*cm, altura_pagina - 10*cm, str(linea_dir1))
    pdf.drawString(3.5*cm, altura_pagina - 10.4*cm, str(linea_dir2))
    pdf.drawString(3.5*cm, altura_pagina - 10.8*cm, str(linea_dir3))
    pdf.drawString(15.5*cm, altura_pagina - 9.35*cm, str(fecha_actual))
    pdf.drawString(14*cm, altura_pagina - 10*cm, 'Evento: '+ str(fecha_evento))
    l = 60
    pdf.drawString(l, 40, str(color_descrip))
    if b.cobras > 0:
        pdf.drawString(14*cm, altura_pagina - 15.25*cm, str(cobras) + ' UND')
    if b.handsfree > 0:
        pdf.drawString(14*cm, altura_pagina - 15.95*cm, str(handsfree) + ' UND')
    if b.cascos > 0:
        pdf.drawString(5*cm, altura_pagina - 17.45*cm, str('Headset Antiruido'))
        pdf.drawString(14*cm, altura_pagina - 17.45*cm, str(cascos + ' UND'))
    if b.baterias > 0:
        pdf.drawString(14*cm, altura_pagina - 19.45*cm, str(baterias) + ' UND')
    if b.cargadores > 0:
        pdf.drawString(14*cm, altura_pagina - 20.15*cm, str(cargadores + ' UND'))
    if b.estaciones >0:
        pdf.drawString(14*cm, altura_pagina - 16.75*cm, str(estaciones + ' UND'))
    if b.repetidoras > 0:
        pdf.drawString(5*cm, altura_pagina - 20.85*cm, str('Repetidoras'))
        pdf.drawString(14*cm, altura_pagina - 20.85*cm, str(repetidoras + ' UND'))
    #radios
    if rx_amarillas > 0:
        pdf.drawString(14*cm, altura_pagina - 11.95*cm, str(amarillas))
        pdf.drawString(14.5*cm, altura_pagina - 11.95*cm, str(' UND'))
    if rx_moradas > 0:
        pdf.drawString(14*cm, altura_pagina - 13.45*cm, str(moradas))
        pdf.drawString(14.5*cm, altura_pagina - 13.45*cm, str(' UND'))
    if rx_plomo > 0:
        pdf.drawString(14*cm, altura_pagina - 12.65*cm, str(plomo))
        pdf.drawString(14.5*cm, altura_pagina - 12.65*cm, str(' UND'))
    # #y = 110
    font_size = 9
    pdf.setFont("Helvetica", font_size)
    x = 60
    h = 60
    f = 60
    g = 60
    # for i in rx:
    #     pdf.drawString(x, 110, str(i))
    #     #y += 20
    #     x += 30
    cuenta_serial = len(rx)
    if cuenta_serial > 16:
        for indice, i in enumerate(rx):
            if indice <15:
                pdf.drawString(x, 80, str(i))
                x += 30
            if indice >15 and indice <31:
                pdf.drawString(h, 70, str(i))
                h += 30
            if indice >31 and indice <47:
                pdf.drawString(f, 60, str(i))
                f += 30
            if indice >47 and indice <60:
                pdf.drawString(g, 50, str(i))
                g += 30
    else:
        for i in rx[:cuenta_serial]:
            pdf.drawString(x, 80, str(i))
            #y += 20
            x += 30

    

    pdf.showPage()

    pdf.save()

    buffer.seek(0)

    nombre_archivo = str(id)+'_'+str(fecha_entrega)+'.pdf'
   
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename= {nombre_archivo}'


    return response

def guardarcolormochila(request, id):

    if request.method == 'POST':

        if mochila.objects.filter(numero_orden=id).exists():
            mochila_color = request.POST.get('mochila')
            mochila_guardada = mochila.objects.get(numero_orden=id)
            mochila_guardada.color = mochila_color
            mochila_guardada.save()
        else:
            mochila_color = request.POST.get('mochila')
            guardamochila = mochila()
            guardamochila.numero_orden = id
            guardamochila.color = mochila_color 
            guardamochila.save()

        color = ""
        if mochila.objects.filter(numero_orden=id).exists():
            mochila_guardada = mochila.objects.get(numero_orden=id)
            color = mochila_guardada.color

        detalle = ordenRegistro.objects.get(id=id)
        return render(request, 'editarOrden.html', {"listaDetalles": detalle, "mochilaguardada":color})

def pdfguiadevueltos(request, id):

    detalle_acce = salidasDetalle.objects.get(id_orden = id)
    b = detalle_acce

    orden = b.id_orden
    salida_id = b.id

    ordenes = ordenRegistro.objects.get(id = orden)

    c = ordenes

    color_mochila = mochila.objects.get(numero_orden = orden)
    color_descrip = color_mochila.color

    fecha_actual = datetime.date.today().strftime('%d/%m/%Y')

    radios = movimientoRadios.objects.filter(id_salida = salida_id, estado = 'F').values_list('serial', flat=True)

    d = radios

    rx_amarillas = vista_movimiento_radios_tipos.objects.filter(id_salida = salida_id, tipo = 'EP 450 (Amarillas)').count()
    rx_moradas =  vista_movimiento_radios_tipos.objects.filter(id_salida = salida_id, tipo = 'DEP 450 (Moradas)').count()
    rx_plomo = vista_movimiento_radios_tipos.objects.filter(id_salida = salida_id, tipo = 'DEP 450 (Plomo)').count()

    amarillas = rx_amarillas
    moradas = rx_moradas
    plomo = rx_plomo



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
    fecha_evento_hasta = (c.fecha_evento_hasta).strftime('%d/%m/%Y')
    direccion = str(c.direccion_entrega)
    rx = d

    buffer = BytesIO()

    pdf = canvas.Canvas(buffer)
    ancho_pagina, altura_pagina = letter = (21.59*cm, 27.94*cm)
    tamano_direccion = len(direccion)

    image_filename = 'logo02.jpg'
    image1_filename = 'logo_cortado.jpg'
    image_path = f'radios/static/{image_filename}'
    image_path1 = f'radios/static/{image1_filename}'


    # Calcula el tamaño y posición de la imagen
    image_width = 60
    image_height = 60
    o = 60
    z = letter[1] - image_height

    image_width01 = 300
    image_height01 = 100

    o = 180
    z2 = z - image_height -45
    

    # Agrega la imagen al documento PDF
    pdf.drawImage(image_path, o, z, width=image_width, height=image_height)
    pdf.drawImage(image_path1, o, z2, width=image_width01, height=image_height01)
    
    if tamano_direccion > 44:
        linea_dir1 = direccion[:44]
        linea_dir2 = direccion[45:88]
        linea_dir3 = direccion[89:133]
    else:
        linea_dir1 = direccion[:44]
        linea_dir2 = ""
        linea_dir3 = "" 

    pdf.drawString(18*cm, altura_pagina - 6.05*cm, 'Salida N°: '+ str(id))
    pdf.drawString(5*cm, altura_pagina - 9.35*cm, 'Cliente: '+ str(cliente))
    pdf.drawString(3.5*cm, altura_pagina - 10*cm, 'Direccion: ' + str(linea_dir1))
    pdf.drawString(3.5*cm, altura_pagina - 10.4*cm, str(linea_dir2))
    pdf.drawString(3.5*cm, altura_pagina - 10.8*cm, str(linea_dir3))
    pdf.drawString(15.5*cm, altura_pagina - 9.35*cm, 'Fecha: ' + str(fecha_actual))
    pdf.drawString(14*cm, altura_pagina - 10*cm, 'Evento: '+ str(fecha_evento))
    pdf.drawString(14*cm, altura_pagina - 10.65*cm, 'Hasta: '+ str(fecha_evento_hasta))
    l = 60
    pdf.drawString(l, 40, str(color_descrip))
    if b.cobras > 0:
        pdf.drawString(14*cm, altura_pagina - 15.25*cm, 'Cobras: '+ str(cobras) + ' UND')
    if b.handsfree > 0:
        pdf.drawString(14*cm, altura_pagina - 15.95*cm, 'HandsFree: '+ str(handsfree) + ' UND')
    if b.cascos > 0:
        pdf.drawString(5*cm, altura_pagina - 17.45*cm, str('Headset Antiruido'))
        pdf.drawString(14*cm, altura_pagina - 17.45*cm, str(cascos + ' UND'))
    if b.baterias > 0:
        pdf.drawString(14*cm, altura_pagina - 19.45*cm, 'Baterias: '+ str(baterias) + ' UND')
    if b.cargadores > 0:
        pdf.drawString(14*cm, altura_pagina - 20.15*cm, 'Cargadores: '+ str(cargadores + ' UND'))
    if b.estaciones >0:
        pdf.drawString(14*cm, altura_pagina - 16.75*cm, 'HandsFree Tipo Escolta: '+ str(estaciones + ' UND'))
    if b.repetidoras > 0:
        pdf.drawString(5*cm, altura_pagina - 20.85*cm, str('Repetidoras'))
        pdf.drawString(14*cm, altura_pagina - 20.85*cm, str(repetidoras + ' UND'))
    #radios
    if rx_amarillas > 0:
        pdf.drawString(10*cm, altura_pagina - 11.95*cm, str('EP 450 (Amarillas)'))
        pdf.drawString(14*cm, altura_pagina - 11.95*cm, str(amarillas))
        pdf.drawString(14.5*cm, altura_pagina - 11.95*cm, str(' UND'))
    if rx_moradas > 0:
        pdf.drawString(10*cm, altura_pagina - 13.45*cm, str('DEP 450 (Moradas)'))
        pdf.drawString(14*cm, altura_pagina - 13.45*cm, str(moradas))
        pdf.drawString(14.5*cm, altura_pagina - 13.45*cm, str(' UND'))
    if rx_plomo > 0:
        pdf.drawString(10*cm, altura_pagina - 12.65*cm, str('DEP 450 (Plomo)'))
        pdf.drawString(14*cm, altura_pagina - 12.65*cm, str(plomo))
        pdf.drawString(14.5*cm, altura_pagina - 12.65*cm, str(' UND'))
    # #y = 110
    font_size = 9
    pdf.setFont("Helvetica", font_size)
    x = 60
    h = 60
    f = 60
    g = 60
    # for i in rx:
    #     pdf.drawString(x, 110, str(i))
    #     #y += 20
    #     x += 30
    cuenta_serial = len(rx)
    if cuenta_serial > 16:
        for indice, i in enumerate(rx): 
            if indice <15:
                pdf.drawString(x, 80, str(i))
                x += 30
            if indice >15 and indice <31:
                pdf.drawString(h, 70, str(i))
                h += 30
            if indice >31 and indice <47:
                pdf.drawString(f, 60, str(i))
                f += 30
            if indice >47 and indice <60:
                pdf.drawString(g, 50, str(i))
                g += 30
    else:
        for i in rx[:cuenta_serial]:
            pdf.drawString(x, 80, str(i))
            #y += 20
            x += 30

    

    pdf.showPage()

    pdf.save()

    buffer.seek(0)

    nombre_archivo = str(id)+'_'+str(fecha_entrega)+'.pdf'
   
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename= {nombre_archivo}'


    return response





    

    






        
      
        

    

 
    




    
