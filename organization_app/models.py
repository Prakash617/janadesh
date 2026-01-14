from django.db import models
import uuid
from django.contrib.auth import get_user_model
from datetime import date
from django.core.exceptions import ValidationError


from django.core.validators import MinValueValidator
from django.utils.text import slugify

User = get_user_model()


# Create your models here.
class Organization(models.Model):
    """Organization/Party profile"""

    name_en = models.CharField(max_length=255)
    name_np = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True)
    description_en = models.TextField()
    description_np = models.TextField(blank=True, null=True)
    logo = models.ImageField(
        upload_to="organization/organization/logo", null=True, blank=True
    )
    banner = models.ImageField(
        upload_to="organization/organization/banner", null=True, blank=True
    )
    established_date = models.DateField(blank=True, null=True)
    manifesto_en = models.TextField(blank=True, null=True)
    manifesto_np = models.TextField(blank=True, null=True)
    manifesto_document = models.FileField(
        upload_to="org_manifestos/", null=True, blank=True
    )
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address_en = models.TextField(blank=True, null=True)
    address_np = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "organizations"

    def __str__(self):
        return self.name_en
    
    
class Branch(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="branches"
    )
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True)

    class Meta:
        unique_together = ("organization", "name")

    def __str__(self):
        return f"{self.name} - {self.organization.name}"
