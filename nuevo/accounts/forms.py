from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class UserAdminCreationForm(UserCreationForm):
    """
    A Custom form for creating new users.
    """

    class Meta:
        model = get_user_model()
        fields = ['email']
        
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'nombre', 'rol', 'codigo_usuario')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rol'].required = True

    def clean(self):
        cleaned_data = super().clean()
        rol = cleaned_data.get('rol')
        if not rol:
            self.add_error('rol', 'Debe seleccionar un rol')
        return cleaned_data      