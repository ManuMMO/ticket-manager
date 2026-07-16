from django.urls import path
from .views import TicketListCreateView, TicketUpdateView, TicketStatsView

urlpatterns = [
    path("tickets/", TicketListCreateView.as_view(), name="tickets-list-create"),
    path("tickets/<int:pk>/", TicketUpdateView.as_view(), name="tickets-update"),
    path("tickets/stats/", TicketStatsView.as_view(), name="tickets-stats"),
]
