from django.db.models import Count
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from gestor.models import Ticket
from .serializers import TicketSerializer

VALID_STATUS = {"open", "in_progress", "closed"}
VALID_PRIORITY = {"low", "medium", "high"}

# GET /api/tickets/  +  POST /api/tickets/
class TicketListCreateView(generics.ListCreateAPIView):
    serializer_class = TicketSerializer

    def get_queryset(self):

        params = self.request.query_params
        errors = {}

        # Validación de nombres de parámetros
        for key in params.keys():
            if key not in ("status", "priority"):
                errors.setdefault("invalid_param", []).append(
                    f"Parámetro no permitido: '{key}'. Usa solo 'status' y/o 'priority'"
                )

        # Validación de los valores
        status = params.get("status")
        if status is not None and status not in VALID_STATUS:
            errors["status_value"] = (
                "Valor inválido para 'status'. "
                "Valores permitidos: 'open', 'in_progress', 'closed'"
            )

        priority = params.get("priority")
        if priority is not None and priority not in VALID_PRIORITY:
            errors["priority_value"] = (
                "Valor inválido para 'priority'. "
                "Valores permitidos: low, medium, high."
            )

        if errors:
            raise ValidationError(errors)

        # Recojo todos los tickets creados por orden descendente de fecha de creación
        qs = Ticket.objects.all().order_by("-created_at")

        # Filtro por el status y la prioridad con params (query_params)
        if status:
            qs = qs.filter(status=status)
        if priority:
            qs = qs.filter(priority=priority)

        return qs


# PATCH /api/tickets/<id>/
class TicketUpdateView(generics.UpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


# GET /api/tickets/stats/
class TicketStatsView(APIView):
    def get(self, request):
        data = (
            Ticket.objects
            .values("status")
            .annotate(count=Count("status"))
            .order_by("status")
        )
        return Response(data)
