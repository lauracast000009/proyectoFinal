from django.db import models
from django.conf import settings

Usuario = settings.AUTH_USER_MODEL

class Conversacion(models.Model):
    estudiante = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="conversaciones")
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    contexto = models.TextField(blank=True)  # texto libre con contexto útil (opcional)

    def __str__(self):
        return f"Conv-{self.id} - {self.estudiante.username} - {self.fecha_inicio.date()}"


class MensajeChat(models.Model):
    EMISOR_CHOICES = (
        ('bot', 'Bot'),
        ('usuario', 'Usuario'),
    )
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE, related_name="mensajes")
    emisor = models.CharField(max_length=10, choices=EMISOR_CHOICES)
    texto = models.TextField()
    creado = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(null=True, blank=True)  # ejemplo: {'pregunta_id': 3}

    def __str__(self):
        return f"{self.emisor}: {self.texto[:30]}"


class Resultado(models.Model):
    estudiante = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="resultados")
    pregunta_id = models.IntegerField()
    respuesta_enviada = models.CharField(max_length=10)
    correcta = models.BooleanField()
    fecha = models.DateTimeField(auto_now_add=True)
    conversacion = models.ForeignKey(Conversacion, on_delete=models.SET_NULL, null=True, blank=True, related_name="resultados")

    def __str__(self):
        return f"R-{self.estudiante.username} - Q{self.pregunta_id} - {'OK' if self.correcta else 'WR'}"
