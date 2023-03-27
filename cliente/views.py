from django.shortcuts import render
from .forms import formCliente
from django.contrib import messages

# Create your views here.
def clientes(request):

    form = formCliente()
    context = {'form':form}
    
    if request.method == 'POST':
        form = formCliente(request.POST)
        if form.is_valid:
            form.save() 
            return render(request,'cliente.html', context)
        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])
                return render(request, 'cliente.html', {"form": form})

    return render(request,'cliente.html', context)