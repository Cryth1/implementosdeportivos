from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from accounts.models import CustomUser

from . import views

urlpatterns = [
    path('estudiante2/', views.estudiante2, name = "estudiante2"),
    path('crearimplemento/', views.crear_implemento, name = "crear_implemento"),
    path('eliminarimplemento/', views.eliminar_implementos, name = "eliminar_implementos"),
    path('prestamos/', views.prestamos, name='prestamos'),
    path('crearprestamo/', views.crear_prestamo, name='crear_prestamo'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('reporte-pdf/', views.generar_reporte_pdf, name='reporte_pdf'),
]