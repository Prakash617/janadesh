from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Manifesto(models.Model):
    """Model to store manifesto PDF files"""

    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
        ("archived", "Archived"),
    )

    # Basic info
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True, help_text="Short description of the manifesto")
    
    # PDF file
    pdf_file = models.FileField(upload_to="manifestos/", help_text="Upload PDF file here")
    
    # Status & timestamps
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Manifesto"
        verbose_name_plural = "Manifestos"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("manifesto_detail", kwargs={"slug": self.slug})

    @property
    def is_published(self):
        return self.status == "published"
