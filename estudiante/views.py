from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

from django.shortcuts import render, redirect

from estudiante.forms import ImplementoDeportivoForm
from accounts.models import CustomUser

from .models import Prestamos

# Create your views here.
@login_required
def estudiante2(request):
    prestamos = Prestamos.objects.filter(IdEstudiante=request.user)

    context = {
        'prestamos': prestamos
    }
    
    
    return render(request, "estudiante2.html", context)

@login_required
@user_passes_test(lambda u: u.rol == CustomUser.Role.FUNCIONARIO, login_url='estudiante2')
def crear_implemento(request):
    
    form = ImplementoDeportivoForm
    if request.method == 'POST':
        form = ImplementoDeportivoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('estudiante2')
    return render(request, 'crearimplemento.html', {'form': form})
