from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

from django.shortcuts import render, redirect

from estudiante.forms import ImplementoDeportivoForm, PrestamoForm
from accounts.models import CustomUser

from .models import Prestamos, ImplementosDeportivos, CategoriasImplementos

# Create your views here.
@login_required
@user_passes_test(lambda u: u.rol == CustomUser.Role.ESTUDIANTE, login_url='dashboard')
def estudiante2(request):
    prestamos = Prestamos.objects.filter(IdEstudiante=request.user)

    context = {
        'prestamos': prestamos
    }
    
    
    return render(request, "estudiante2.html", context)

@login_required
@user_passes_test(lambda u: u.rol == CustomUser.Role.FUNCIONARIO, login_url='estudiante2')
def dashboard(request):
    return render(request, "dashboard.html")

@login_required
@user_passes_test(lambda u: u.rol == CustomUser.Role.FUNCIONARIO, login_url='estudiante2')
def prestamos(request):
    prestamos = Prestamos.objects.all()

    context = {
        'prestamos': prestamos
    }

    return render(request, "prestamos.html", context)

@login_required
@user_passes_test(lambda u: u.rol == CustomUser.Role.FUNCIONARIO, login_url='estudiante2')
def crear_prestamo(request):
    if request.method == 'POST':
        form = PrestamoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crear_prestamo')
    else:
        form = PrestamoForm()
    
    return render(request, 'loan_creation.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.rol == CustomUser.Role.FUNCIONARIO, login_url='estudiante2')
def crear_implemento(request):
    
    form = ImplementoDeportivoForm
    if request.method == 'POST':
        form = ImplementoDeportivoForm(request.POST)
        print(form.is_valid())
        print(form.errors)
        if form.is_valid():
            cantidad = form.cleaned_data.get('cantidad')
            for i in range(cantidad):
                implemento = form.save(commit=False)
                implemento.id_implemento = None
                implemento.save()
            return redirect('prestamos')    
    categorias = CategoriasImplementos.objects.all()
    return render(request, 'crearimplemento.html', {'form': form, 'categorias':categorias})



@login_required
@user_passes_test(lambda u: u.rol == CustomUser.Role.FUNCIONARIO, login_url='estudiante2')
def eliminar_implementos(request):
    if request.method == 'POST':
        implementos_ids = request.POST.getlist('implementos_ids')
        ImplementosDeportivos.objects.filter(pk__in=implementos_ids).delete()
        return redirect('eliminar_implementos')
    
    implementos = ImplementosDeportivos.objects.all()
    return render(request, 'eliminarimplemento.html', {'implementos': implementos})
