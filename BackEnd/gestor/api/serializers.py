from rest_framework import serializers
from gestor.models import Ticket

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"

    # DRF detecta validación en el campo status por defecto.
    def validate_status(self, value):
        
        # Regla: No se puede crear un ticket cerrado
        if self.instance is None and value == "closed":
            raise serializers.ValidationError(
                "Un ticket no puede crearse con el estado 'Cerrado'. Debe crearse como 'Abierto' o 'En progreso'."
            )
        return value

    def update(self, instance, validated_data):
        new_status = validated_data.get("status", instance.status)

        # Regla: Un ticket cerrado no puede volver al estado Abierto
        if instance.status == "closed" and new_status == "open":
            
            # Los errores lanzados en update() no se asocian a ningún campo. Hay que indicar 'status' manualmente.
            raise serializers.ValidationError({
                "status" : "Un ticket 'cerrado'' no puede volver al estado 'Abierto' directamente. Debe pasar por 'En progreso'."
            })

        return super().update(instance, validated_data)
