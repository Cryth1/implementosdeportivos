from django.db import models

from accounts.models import CustomUser

# Create your models here.


class ClubDeportivo(models.Model):
    id_club = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20)
    
    def __str__(self):   
        return self.nombre       


class CategoriasImplementos(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20)
    club_deportivo = models.ForeignKey(ClubDeportivo, on_delete=models.CASCADE, default = None)
    
    def __str__(self):
        return self.nombre



class ImplementosDeportivos(models.Model):
    id_implemento = models.AutoField(primary_key=True)
    id_categoria = models.ForeignKey(CategoriasImplementos, on_delete=models.CASCADE)
    marca = models.CharField(max_length=20)
    disponibilidad = models.BooleanField()
    
    def __str__(self):
        return self.id_categoria.nombre + " Marca: " + self.marca + " id: " + str(self.id_implemento)


    
    
class Prestamos(models.Model):
    ESTADO_CHOICES = (
        ('prestamo', 'En préstamo'),
        ('devuelto', 'Devuelto'),
        ('vencido', 'Vencido'),
    )
    
    IdPrestamo = models.AutoField(primary_key=True)
    IdEstudiante = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    IdImplemento = models.ForeignKey(ImplementosDeportivos, on_delete=models.CASCADE)
    Estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='prestamo')
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