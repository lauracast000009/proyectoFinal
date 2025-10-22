from rest_framework import serializers
from .models import Conversacion, MensajeChat, Resultado


class MensajeChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = MensajeChat
        fields = '__all__'
        read_only_fields = ('creado',)


class ConversacionSerializer(serializers.ModelSerializer):
    mensajes = MensajeChatSerializer(many=True, read_only=True)

    class Meta:
        model = Conversacion
        fields = '__all__'
        # 🔹 Muy importante incluir estudiante como solo lectura
        read_only_fields = ('fecha_inicio', 'estudiante')


class ResultadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resultado
        fields = '__all__'
        # 🔹 También aquí estudiante debe ser de solo lectura
        read_only_fields = ('fecha', 'estudiante')
