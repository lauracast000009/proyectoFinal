from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Leccion, Pregunta
from .serializers import LeccionSerializer, PreguntaSerializer

class LeccionViewSet(viewsets.ModelViewSet):
    queryset = Leccion.objects.all()
    serializer_class = LeccionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(docente=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Leccion.objects.all()
        elif user.role == 'docente':
            return Leccion.objects.filter(docente=user)
        else:  # estudiante
            return Leccion.objects.all()


class PreguntaViewSet(viewsets.ModelViewSet):
    serializer_class = PreguntaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = Pregunta.objects.select_related('leccion', 'leccion__docente')

        if user.role == 'admin':
            return qs
        elif user.role == 'docente':
            return qs.filter(leccion__docente=user)
        elif hasattr(user, 'grado') and user.grado:
            return qs.filter(leccion__grado=user.grado)
        return qs.none()

    def perform_update(self, serializer):
        """Permitir que el docente solo modifique preguntas de sus propias lecciones"""
        pregunta = self.get_object()
        user = self.request.user
        if user.role == 'docente' and pregunta.leccion.docente != user:
            raise PermissionDenied("No puedes modificar preguntas de otra lección.")
        serializer.save()

    def perform_destroy(self, instance):
        """Permitir que el docente solo elimine sus propias preguntas"""
        user = self.request.user
        if user.role == 'docente' and instance.leccion.docente != user:
            raise PermissionDenied("No puedes eliminar preguntas de otra lección.")
        instance.delete()