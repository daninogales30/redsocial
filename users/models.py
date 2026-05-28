from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

class User(AbstractUser):
    username = models.CharField(
        max_length=20,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9_]+$',
                message='Solo letras, números y _'
            )
        ]
    )
    email = models.EmailField(unique=True)
    bio = models.TextField(
        blank=True,
        null=True,
    )
    foto_perfil = models.ImageField(
        upload_to='perfiles/',
        default='default.png',
        blank=True,
        null=True,
    )

