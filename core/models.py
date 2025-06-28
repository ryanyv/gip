from django.conf import settings
from django.db import models


class TeamMember(models.Model):
    """Represents a user that should appear on the About page."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return str(self.user)
