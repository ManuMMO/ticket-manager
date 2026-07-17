import pytest
from rest_framework import status
from gestor.models import Ticket

@pytest.mark.django_db
def test_cannot_create_ticket_with_closed_status(client):
    payload = {
        "title": "Intento inválido",
        "status": "closed",
        "priority": "medium",
    }

    response = client.post("/api/tickets/", payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "status" in response.data
    assert Ticket.objects.count() == 0


@pytest.mark.django_db
def test_closed_ticket_cannot_go_back_to_open_directly(client):
    ticket = Ticket.objects.create(
        title="Ticket cerrado",
        status="closed",
        priority="high",
    )

    response = client.patch(
        f"/api/tickets/{ticket.id}/",
        {"status": "open"},
        content_type="application/json"
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "status" in response.data

    ticket.refresh_from_db()
    assert ticket.status == "closed"