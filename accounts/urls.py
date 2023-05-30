from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

from django.contrib.auth import views as auth_views
from accounts import views
from accounts.views import ChangePasswordView

urlpatterns = [

    path('register/', views.register, name = "register"),
    path('login/', views.loginf, name="login"),
    path('profile/', views.profile, name='profile'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('delete_user/', views.delete_user, name = 'delete_user'),
    path('', include('django.contrib.auth.urls')),
    path('redirigir_prestamos/', views.redirigir_prestamos, name='redirigir_prestamos'),
   

]