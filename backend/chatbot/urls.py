from django.urls import path
from .views import (
    IniciarConversacionView, EnviarMensajeView, HistorialConversacionView,
    ConversacionesPorEstudianteView, EvaluarRespuestaManualView
)

urlpatterns = [
    path('conversacion/iniciar/', IniciarConversacionView.as_view(), name='chat-iniciar'),
    path('mensaje/', EnviarMensajeView.as_view(), name='chat-mensaje'),
    path('conversacion/<int:pk>/historial/', HistorialConversacionView.as_view(), name='chat-historial'),
    path('conversaciones/', ConversacionesPorEstudianteView.as_view(), name='chat-conversaciones'),
    path('respuesta/evaluar/', EvaluarRespuestaManualView.as_view(), name='chat-evaluar'),
]
