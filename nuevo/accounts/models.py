from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    
    class Role(models.TextChoices):
        ESTUDIANTE = "ESTUDIANTE", "Estudiante"
        FUNCIONARIO = "FUNCIONARIO", "Funcionario"
    

    codigo_usuario = models.CharField(_('codigo de usuario'), max_length=20, unique=True, default='0000')
    nombre = models.CharField(_('nombre'),max_length=20, default = '')
    rol = models.CharField(max_length=20, choices=Role.choices, default=Role.ESTUDIANTE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['codigo_usuario', 'nombre']

    objects = CustomUserManager()


    


class CategoriasImplementos(models.Model):
    IdCategoria = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=20)


class EstadoImplemento(models.Model):
    IdEstado = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=20)
    
    
class ImplementosDeportivos(models.Model):
    Idimplemento = models.AutoField(primary_key=True)
    IdCategoria = models.ForeignKey(CategoriasImplementos, on_delete=models.CASCADE)
    IdEstado = models.ForeignKey(EstadoImplemento, on_delete=models.CASCADE)
    Marca = models.CharField(max_length=20)
    Disponibilidad = models.BooleanField()
    
class Prestamos(models.Model):
    IdPrestamo = models.AutoField(primary_key=True)
    IdEstudiante = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    IdImplemento = models.ForeignKey(ImplementosDeportivos, on_delete=models.CASCADE)
    FechaPrestamo = models.DateTimeField()
    FechaDevolucion = models.DateTimeField()
    


class Reservas(models.Model):
    IdReserva = models.AutoField(primary_key=True)
    IdPrestamo = models.ForeignKey(Prestamos, on_delete=models.CASCADE)
    FechaDeSolicitud = models.DateTimeField()
    IdImplemento = models.ForeignKey(ImplementosDeportivos, on_delete=models.CASCADE)
    Aprobado = models.BooleanField(null=True)

class TiposDeMulta(models.Model):
    IdTipo = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=20)
    Valor = models.DecimalField(max_digits=10, decimal_places=2)
    
class Multas(models.Model):
    IdMulta = models.AutoField(primary_key=True)
    IdEstudiantes = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    IdTipo = models.ForeignKey(TiposDeMulta, on_delete=models.CASCADE)
    Sancion = models.CharField(max_length=20)
    Descripcion = models.TextField(max_length=200)
    Pagada = models.BooleanField()


class Devoluciones(models.Model):
    IDestudiante = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    IDimplemento = models.ForeignKey(ImplementosDeportivos, on_delete=models.CASCADE)
    FechaEntrega = models.DateTimeField()
    prestamo = models.IntegerField()
    class Meta:
        unique_together = (("IDestudiante", "IDimplemento"),)