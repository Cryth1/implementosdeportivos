from django.contrib import admin
from .models import CategoriasImplementos, ImplementosDeportivos, Prestamos, ClubDeportivo

# Register your models here.


admin.site.register(CategoriasImplementos)
admin.site.register(ClubDeportivo)


class ImplementosDeportivosAdmin(admin.ModelAdmin):
    list_display = ['id_implemento', 'id_categoria', 'marca', 'disponibilidad']
    list_filter = ['id_categoria', 'disponibilidad']
    search_fields = ['marca']
    
class PrestamosAdmin(admin.ModelAdmin):
    list_display = ['IdPrestamo', 'IdEstudiante', 'IdImplemento', 'Estado', 'FechaPrestamo', 'FechaDevolucion']
    list_filter = ['IdEstudiante', 'IdImplemento', 'Estado', 'FechaPrestamo']
    search_fields = ['IdPrestamo']
    
admin.site.register(ImplementosDeportivos, ImplementosDeportivosAdmin)
admin.site.register(Prestamos, PrestamosAdmin)