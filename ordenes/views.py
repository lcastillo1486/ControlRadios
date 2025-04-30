from django.shortcuts import render, HttpResponse, redirect
from .forms import formOrden, formEdit, formEditFactura
from django.contrib import messages
from .models import ordenRegistro
from movimientos.models import auditoria
from django.utils import timezone
# Create your views here.


def ordenes(request):

    form = formOrden()
    context = {'form_orden': form}

    if request.method == 'POST':
        form = formOrden(request.POST)
        if form.is_valid():
            a = form.save(commit=False)
            a.estado_id = 2
            a.save()
###AUDITORIA#######
            #buscar el ultimo id generado
            ultimo_id = ordenRegistro.objects.latest('id').id
            #capturar usuario actual
            user_nombre = request.user.username
            #fecha y hora actual
            fecha_hora_peru = timezone.localtime(timezone.now())
            fecha_hora_formateada = fecha_hora_peru.strftime('%Y-%m-%d %H:%M:%S')

            log = auditoria(fecha = fecha_hora_formateada, accion = f'Orden Creada N° {ultimo_id}', usuario = user_nombre)
            log.save()


            
            return render(request, 'ordenes.html', context)
        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])
                return render(request, 'ordenes.html', {"form": form})

    return render(request, 'ordenes.html', context)


def buscaEdit(request, id_orden):

    editCurso = ordenRegistro.objects.get(id = id_orden)
    form = formEdit(instance=editCurso)

    if editCurso.estado_id == 5:
    
         return HttpResponse('Esta orden ya ha sido procesada. No se puede modificar')

    if request.method == 'POST':

        form = formEdit(request.POST,instance=editCurso)
        if form.is_valid:
            form.save()

###AUDITORIA#######
            #buscar el ultimo id generado
            #ultimo_id = id_orden
            #capturar usuario actual
            #user_nombre = request.user.username
            #fecha y hora actual
            #fecha_hora_peru = timezone.localtime(timezone.now())
            #fecha_hora_formateada = fecha_hora_peru.strftime('%Y-%m-%d %H:%M:%S')

            #log = auditoria(fecha = fecha_hora_formateada, accion = f'Orden Modificada N° {ultimo_id}', usuario = user_nombre)
            #log.save()
 

    editCurso = ordenRegistro.objects.get(id = id_orden)
    form = formEdit(instance=editCurso)

    #return redirect('salidas/')

    return render(request,'modificaOrden.html',{"form_orden":form})

def buscaEditFactura(request, id_orden):

    editCurso = ordenRegistro.objects.get(id = id_orden)
    form = formEditFactura(instance=editCurso)

    if request.method == 'POST':
        form = formEditFactura(request.POST,instance=editCurso)
        if form.is_valid:
            form.save()
            return redirect('/listadocxc/')

    editCurso = ordenRegistro.objects.get(id = id_orden)
    form = formEditFactura(instance=editCurso)

    return render(request,'editpedidofactura.html',{"form_orden":form})




