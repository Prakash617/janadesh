from django.db import models
from tinymce.models import HTMLField

# Create your models here.
class Service(models.Model):
    """Service management for personal/organizational websites"""
    title_en = models.CharField(max_length=255)
    title_np = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True)
    description_en = HTMLField(blank=True, null=True)
    description_np = HTMLField(blank=True, null=True)
    icon = models.CharField(max_length=100, blank=True, null=True, help_text="Icon class or image")
    image = models.ImageField(upload_to='services/service/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'services'
        ordering = ['order', '-created_at']
        verbose_name = 'Service'
        verbose_name_plural = 'Service'

    def __str__(self):
        return self.title_en