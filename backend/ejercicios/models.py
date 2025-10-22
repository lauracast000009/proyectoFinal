from django.db import models
from django.conf import settings

Usuario = settings.AUTH_USER_MODEL

class Leccion(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    grado = models.CharField(max_length=20)
    tema = models.CharField(max_length=50)
    docente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="lecciones")

    def __str__(self):
        return f"{self.titulo} ({self.grado})"


class Pregunta(models.Model):
    leccion = models.ForeignKey(Leccion, on_delete=models.CASCADE, related_name="preguntas")
    texto = models.TextField()
    opcion_a = models.CharField(max_length=200)
    opcion_b = models.CharField(max_length=200)
    opcion_c = models.CharField(max_length=200)
    opcion_d = models.CharField(max_length=200)
    respuesta_correcta = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])

    def __str__(self):
        return f"Pregunta {self.id} - {self.leccion.titulo}"
