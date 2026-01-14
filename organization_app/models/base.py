from django.db import models


class OrgBranchBaseModel(models.Model):
    organization = models.ForeignKey(
        "organization_app.Organization",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    branch = models.ForeignKey(
        "organization_app.Branch",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        abstract = True
