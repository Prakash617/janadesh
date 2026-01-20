from django.db import models
from django.contrib.auth.models import Permission

class Role(models.Model):
    name = models.CharField(max_length=100)
    organization = models.ForeignKey(
        "organization_app.Organization",
        on_delete=models.CASCADE,
        related_name="roles"
    )
    permissions = models.ManyToManyField(
        Permission,
        blank=True
    )

    class Meta:
        unique_together = ("organization", "name")
        verbose_name = "Role"
        verbose_name_plural = "Role"

    def __str__(self):
        return f"{self.name} ({self.organization})"