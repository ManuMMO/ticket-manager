from django.db import models

class Ticket(models.Model):
    PRIORITY_CHOICES = [
        ("low", "Baja"),
        ("medium", "Media"),
        ("high", "Alta"),
    ]

    STATUS_CHOICES = [
        ("open", "Abierto"),
        ("in_progress", "En progreso"),
        ("closed", "Cerrado"),
    ]

    title = models.CharField("Título", max_length=120)
    description = models.TextField("Descripción", blank=True)
    priority = models.CharField("Prioridad", max_length=10, choices=PRIORITY_CHOICES)
    status = models.CharField(
        "Estado",
        max_length=20,
        choices=STATUS_CHOICES,
        default="open",
    )
    created_at = models.DateTimeField("Creado en", auto_now_add=True)
    updated_at = models.DateTimeField("Actualizado en", auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
