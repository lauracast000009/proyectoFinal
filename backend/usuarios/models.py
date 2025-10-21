from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Administrador'),
        ('docente', 'Docente'),
        ('estudiante', 'Estudiante'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='estudiante')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    grado = models.CharField(max_length=20, null=True, blank=True)  # solo estudiantes
    area = models.CharField(max_length=50, null=True, blank=True)   # solo docentes

    def __str__(self):
        return f"{self.username} ({self.role})"
