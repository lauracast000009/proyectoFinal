from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Conversacion, MensajeChat, Resultado
from .serializers import ConversacionSerializer, MensajeChatSerializer, ResultadoSerializer
from ejercicios.models import Pregunta, Leccion
from chatbot.logic.respuestas import obtener_siguiente_pregunta_por_leccion, evaluar_respuesta
from django.shortcuts import get_object_or_404

class IniciarConversacionView(generics.CreateAPIView):
    serializer_class = ConversacionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(estudiante=self.request.user)

class EnviarMensajeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Recibe: { 'conversacion': <id|null>, 'texto': str, 'tipo': 'respuesta'|'consulta', 'meta': {...} }
        Responde con mensaje del bot y guarda ambos mensajes.
        """
        user = request.user
        texto = request.data.get('texto', '').strip()
        conv_id = request.data.get('conversacion')
        tipo = request.data.get('tipo', 'consulta')
        meta = request.data.get('meta', {})

        # obtener o crear conversacion
        if conv_id:
            conversacion = get_object_or_404(Conversacion, id=conv_id, estudiante=user)
        else:
            conversacion = Conversacion.objects.create(estudiante=user)

        # guardar mensaje del usuario
        user_msg = MensajeChat.objects.create(conversacion=conversacion, emisor='usuario', texto=texto, metadata=meta)

        # Simple logic:
        # meta puede traer {'leccion_id': X, 'ultima_pregunta_ids': [..], 'pregunta_id': N} si aplica
        leccion_id = meta.get('leccion_id')
        ultima_pregunta_id = meta.get('pregunta_id')

        # Si el usuario envía una respuesta a una pregunta previa:
        if tipo == 'respuesta' and ultima_pregunta_id:
            pregunta = get_object_or_404(Pregunta, id=ultima_pregunta_id)
            resultado = evaluar_respuesta(pregunta, texto)
            Resultado.objects.create(
                estudiante=user,
                pregunta_id=pregunta.id,
                respuesta_enviada=texto,
                correcta=resultado['correcta'],
                conversacion=conversacion
            )
            bot_text = resultado['feedback']

            # preparar siguiente pregunta si estaba la lección
            if leccion_id:
                siguiente = obtener_siguiente_pregunta_por_leccion(leccion_id, exclude_ids=[ultima_pregunta_id])
                if siguiente:
                    bot_text += f"\n\nSiguiente pregunta:\nID={siguiente.id} - {siguiente.texto}\nA) {siguiente.opcion_a}\nB) {siguiente.opcion_b}\nC) {siguiente.opcion_c}\nD) {siguiente.opcion_d}"
                    bot_meta = {'pregunta_id': siguiente.id, 'leccion_id': leccion_id}
                else:
                    bot_text += "\n\nNo hay más preguntas en esta lección."
                    bot_meta = {}
            else:
                bot_meta = {}

        else:
            # tipo consulta / pedir pregunta desde 0
            if leccion_id:
                siguiente = obtener_siguiente_pregunta_por_leccion(leccion_id)
                if siguiente:
                    bot_text = f"{siguiente.texto}\nA) {siguiente.opcion_a}\nB) {siguiente.opcion_b}\nC) {siguiente.opcion_c}\nD) {siguiente.opcion_d}"
                    bot_meta = {'pregunta_id': siguiente.id, 'leccion_id': leccion_id}
                else:
                    bot_text = "No encontré preguntas para esa lección."
                    bot_meta = {}
            else:
                bot_text = "Hola, ¿en qué lección quieres practicar? Envia {\"leccion_id\": X} en meta."
                bot_meta = {}

        bot_msg = MensajeChat.objects.create(conversacion=conversacion, emisor='bot', texto=bot_text, metadata=bot_meta)

        return Response({
            'conversacion': ConversacionSerializer(conversacion).data,
            'mensaje_bot': MensajeChatSerializer(bot_msg).data
        }, status=status.HTTP_200_OK)


class HistorialConversacionView(generics.RetrieveAPIView):
    queryset = Conversacion.objects.all()
    serializer_class = ConversacionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        conv = super().get_object()
        if conv.estudiante != self.request.user and self.request.user.role != 'admin':
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("No puedes ver esta conversación.")
        return conv

class ConversacionesPorEstudianteView(generics.ListAPIView):
    serializer_class = ConversacionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Conversacion.objects.all()
        return Conversacion.objects.filter(estudiante=user)

class EvaluarRespuestaManualView(generics.CreateAPIView):
    """
    Endpoint opcional para enviar evaluación manual si necesitas lógica custom.
    """
    serializer_class = ResultadoSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(estudiante=self.request.user)
