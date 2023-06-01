from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count  
from django.shortcuts import render, redirect
from django.urls import reverse
from django.templatetags.static import static

import os

from estudiante.forms import ImplementoDeportivoForm, PrestamoForm
from accounts.models import CustomUser

from .models import Prestamos, ImplementosDeportivos, CategoriasImplementos
from django.http import FileResponse, HttpResponse

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle 

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

from io import BytesIO

import concurrent.futures
import time
import threading




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
def generar_reporte_pdf(request):
  
    if request.user.rol == CustomUser.Role.ESTUDIANTE:
    
        prestamos = Prestamos.objects.filter(IdEstudiante=request.user)
    elif request.user.rol == CustomUser.Role.FUNCIONARIO:
      
        prestamos = Prestamos.objects.all()



     
    buffer = BytesIO()

  
    doc = SimpleDocTemplate(buffer, pagesize=letter)


    data = []


    headers = ["Nombre","Estado", "Categoría", "Implemento", "Fecha de Préstamo", "Fecha de Devolución"]
    data.append(headers)

   
    for prestamo in prestamos:
        row = [
            prestamo.IdEstudiante.nombre,
            prestamo.get_Estado_display(),
            prestamo.IdImplemento.id_categoria.club_deportivo.nombre,
            prestamo.IdImplemento.id_categoria.nombre,
            str(prestamo.FechaPrestamo),
            str(prestamo.FechaDevolucion),
        ]
        data.append(row)


    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])


    table = Table(data)
    table.setStyle(table_style)


    elements = [table]
    doc.build(elements)

 
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte.pdf"'

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response


def generar_grafico():
    datos = Prestamos.objects.values('Estado').annotate(count=Count('Estado'))
    prestamos_realizados = 0
    prestamos_vencidos = 0
    
    for dato in datos:
        if dato['Estado'] == 'prestamo':
            prestamos_realizados = dato['count']
        elif dato['Estado'] == 'vencido':
            prestamos_vencidos = dato['count']
    
    
    etiquetas = ['Realizados', 'Vencidos']
    valores = [prestamos_realizados, prestamos_vencidos]
    
    plt.bar(etiquetas, valores)
    plt.xlabel('Estado')
    plt.ylabel('Cantidad')
    plt.title('Préstamos realizados y vencidos')
    
  
    ruta_archivo = 'estudiante/static/estudiante/img/prestamos.png'
    plt.savefig(ruta_archivo)
    

@login_required
@user_passes_test(lambda u: u.rol == CustomUser.Role.FUNCIONARIO, login_url='estudiante2')
def dashboard(request):
    
    timestamp = str(int(time.time()))
    
    generar_grafico()
    
    implementos_prestados = Prestamos.objects.count()
    prestamos_vencidos = Prestamos.objects.filter(Estado='vencido').count()
    
    
    ruta_archivo = os.path.join('estudiante', 'img', 'prestamos.png')
    

    ruta_completa = static(ruta_archivo) + '?t=' + timestamp

   
   
    context = {'ruta_archivo':ruta_completa, 'implementos_prestados': implementos_prestados, 'prestamos_vencidos': prestamos_vencidos}
    
    return render(request, "dashboard.html", context)

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
