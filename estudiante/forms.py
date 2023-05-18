from django import forms
from .models import ImplementosDeportivos


class ImplementoDeportivoForm(forms.ModelForm):
    class Meta:
        model = ImplementosDeportivos
        fields = '__all__'