from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from accounts.forms import UserAdminCreationForm, CustomUserCreationForm


from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required

from django.db.models import Q
from estudiante.views import prestamos





class ChangePasswordView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'change_password.html'
    success_url = '/profile/'
    
    
    
def redirigir_prestamos(request):
    return redirect('prestamos')

def delete_user(request):
    if request.method == 'POST':
        user = request.user # obtiene el usuario actual
        user.delete()
        return redirect('/accounts/login')
    return render(request, 'delete_user.html')




def register(request):
    if request.user.is_authenticated:
        return redirect('estudiante2')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('estudiante2')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


def loginf(req):
    
    if req.user.is_authenticated:
        return redirect('estudiante2')
    
    if req.method == 'POST':
        email = req.POST.get('email')
        password = req.POST.get('password')
        user = authenticate(req, email=email, password = password )
        if user is not None:
            login(req,user)
            return redirect('estudiante2')   
        else:
            messages.error(req, 'Usuario no existe o contraseña incorrecta. Verifica que tus credenciales sean correctas' ) 
    return render(req, 'registration/login.html')


@login_required
def profile(request):
    user = request.user
    edit_mode = False
    if request.method == 'POST':
        if 'edit' in request.POST:
            edit_mode = True
        elif 'cancel' in request.POST:
            edit_mode = False
        else:
            new_email = request.POST['email']
            new_codigo_usuario = request.POST['codigo_usuario']
            new_nombre = request.POST['nombre']
            # Comprobar si los nuevos datos ya existen en la base de datos
            if get_user_model().objects.exclude(id=user.id).filter(
                Q(email=new_email) | Q(codigo_usuario=new_codigo_usuario)
            ).exists():
                messages.error(request, 'El email o el código de usuario ya existen en la base de datos. No se ha guardado ningún cambio')
            else:
                user.email = new_email
                user.codigo_usuario = new_codigo_usuario
                user.nombre = new_nombre
                user.save()
                edit_mode = False
    context = {
        'user': user,
        'edit_mode': edit_mode,
    }
    return render(request, 'profile.html', context)

# @login_required
# def estudiante2(request):
#     return render(request, "estudiante2.html")