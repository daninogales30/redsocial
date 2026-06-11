from django import forms
from django.utils import timezone

from .models import User

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "Usuario"
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Contraseña"
        })
    )

class RegisterForm(forms.Form):
    email = forms.EmailField(label="Correo electrónico", widget=forms.EmailInput(attrs={'placeholder': 'Correo electrónico'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}), label="Contraseña")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Repetir contraseña'}), label="Confirmar contraseña")
    fecha_nacimiento = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Fecha de nacimiento"
    )
    nombre = forms.CharField(max_length=100, label="Nombre", widget=forms.TextInput(attrs={'placeholder': 'Nombre'}))
    username = forms.CharField(max_length=150, label="Usuario", widget=forms.TextInput(attrs={'placeholder': 'Nombre usuario'}))
    foto_perfil = forms.ImageField(required=False, label="Foto de perfil")



    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Este nombre de usuario ya está en uso.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado.')
        return email

    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data.get('fecha_nacimiento')
        if fecha and fecha > timezone.now().date():
            raise forms.ValidationError('La fecha de nacimiento no puede ser futura.')
        return fecha

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Las contraseñas no coinciden.')
        return cleaned_data