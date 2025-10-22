# logic/respuestas.py
from ejercicios.models import Pregunta, Leccion

def obtener_siguiente_pregunta_por_leccion(leccion_id, exclude_ids=None):
    """
    Devuelve la siguiente pregunta disponible (obj Pregunta) para la lección,
    excluyendo ids en exclude_ids (lista).
    """
    qs = Pregunta.objects.filter(leccion_id=leccion_id)
    if exclude_ids:
        qs = qs.exclude(id__in=exclude_ids)
    return qs.first()  # simple: la primera. Puedes cambiar a .order_by('?') para aleatoria

def evaluar_respuesta(pregunta: Pregunta, respuesta_texto: str):
    """Evalúa si la respuesta enviada (A/B/C/D o texto) es correcta."""
    enviado = respuesta_texto.strip().upper()
    correcta = pregunta.respuesta_correcta.upper() == enviado
    feedback = "Correcto ✅" if correcta else f"Incorrecto ❌. La respuesta correcta es {pregunta.respuesta_correcta}."
    # Puedes añadir explicación aquí si tu modelo Pregunta tuviera campo 'explicacion'
    return {
        "correcta": correcta,
        "feedback": feedback
    }
