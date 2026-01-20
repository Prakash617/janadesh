import uuid
from django.db import models
from tinymce.models import HTMLField


# class Organization(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=255, unique=True)
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name
    
    
class Organization(models.Model):
    """Organization/Party profile"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name_en = models.CharField(max_length=255)
    name_np = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True)
    description_en = HTMLField(blank=True, null=True)
    description_np = HTMLField(blank=True, null=True)
    logo = models.ImageField(
        upload_to="organization/organization/logo", null=True, blank=True
    )
    banner = models.ImageField(
        upload_to="organization/organization/banner", null=True, blank=True
    )
    established_date = models.DateField(blank=True, null=True)
    manifesto_en = HTMLField(blank=True, null=True)
    manifesto_np = HTMLField(blank=True, null=True)
    manifesto_document = models.FileField(
        upload_to="org_manifestos/", null=True, blank=True
    )
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address_en = HTMLField(blank=True, null=True)
    address_np = HTMLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "organization"
        verbose_name = "Organization"
        verbose_name_plural = "Organization"

    def __str__(self):
        return self.name_en
