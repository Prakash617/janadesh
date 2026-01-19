import uuid
from django.db import models


class Branch(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(
        "organization_app.Organization",
        on_delete=models.CASCADE,
        related_name="branches"
    )
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True)

    class Meta:
        unique_together = ("organization", "name")

    def __str__(self):
        return f"{self.name} ({self.organization.name_en})"
