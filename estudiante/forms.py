from django import forms
from .models import ImplementosDeportivos, Prestamos


class ImplementoDeportivoForm(forms.ModelForm):
    cantidad = forms.IntegerField(required=True)
    class Meta:
        model = ImplementosDeportivos
        fields = '__all__'
        
        
class PrestamoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['FechaPrestamo'].widget = forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        self.fields['FechaDevolucion'].widget = forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})

    class Meta:
        model = Prestamos
        fields = ['IdEstudiante', 'IdImplemento', 'Estado', 'FechaPrestamo', 'FechaDevolucion']
        