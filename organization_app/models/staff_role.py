from django.db import models
from django.conf import settings


class StaffRole(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="staff_role"
    )
    role = models.ForeignKey(
        "organization_app.Role",
        on_delete=models.CASCADE,
        related_name="staff_members"
    )

    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} → {self.role}"
