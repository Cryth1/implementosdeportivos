from django import forms
from .models import ImplementosDeportivos


class ImplementoDeportivoForm(forms.ModelForm):
    cantidad = forms.IntegerField(required=True)
    class Meta:
        model = ImplementosDeportivos
        fields = '__all__'