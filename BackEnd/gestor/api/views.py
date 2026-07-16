from django.db.models import Count
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from gestor.models import Ticket
from .serializers import TicketSerializer


# GET /api/tickets/  +  POST /api/tickets/
class TicketListCreateView(generics.ListCreateAPIView):
    serializer_class = TicketSerializer

    def get_queryset(self):
        # Recojo todos los tickets creados por orden descendente de fecha de creación
        qs = Ticket.objects.all().order_by("-created_at")

        # Filtro por el status y la prioridad con query_params
        status = self.request.query_params.get("status")
        priority = self.request.query_params.get("priority")

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
