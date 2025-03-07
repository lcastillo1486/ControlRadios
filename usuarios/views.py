from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

def registro(request):

    if request.method == 'GET':
        return render(request, 'registro.html', {'registro_form': UserCreationForm})

    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                return redirect('inicial')
            except:
                return render(request, 'registro.html', {'registro_form': UserCreationForm, 'error': 'El usuario ya existe'})

        return HttpResponse('Las contraeñas no coinciden')

def logear(request):

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            nombre_usuario = form.cleaned_data.get("username")
            contra = form.cleaned_data.get("password")
            usuario = authenticate(username=nombre_usuario, password=contra)
            if usuario is not None:
                login(request, usuario)
                if nombre_usuario == 'monitor':
                    return redirect('monitor/')
                if nombre_usuario == 'monitoreo':
                    return redirect('api/cajas/')
                return redirect('salidas/')
            else:
                for msg in form.error_messages:
                    messages.error(request,form.error_messages[msg])
                    return render(request, 'home.html', {"form": form})
        else:
            for msg in form.error_messages:
                    messages.error(request,form.error_messages[msg])
                    return render(request, 'home.html', {"form": form})

    form = AuthenticationForm()
    return render(request, 'home.html', {"form": form})

def inicio(request):
    return render(request, 'inicio.html')

def cerrarSesion(request):
    logout(request)
    return redirect('inicial')
