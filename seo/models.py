from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class SEOMetadata(models.Model):
    """SEO metadata for any model"""
# Choose content_type = blog

# Set object_id = blog.id

    # REQUIRED for GenericForeignKey
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE    #give modal name
    )
    object_id = models.PositiveIntegerField()  # give model instance id 
    content_object = GenericForeignKey("content_type", "object_id")  # python function that return actual object

    # SEO fields
    meta_title_en = models.CharField(max_length=255, blank=True, null=True)
    meta_title_np = models.CharField(max_length=255, blank=True, null=True)
    meta_description_en = models.TextField(blank=True, null=True)
    meta_description_np = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)

    og_title_en = models.CharField(max_length=255, blank=True, null=True)
    og_title_np = models.CharField(max_length=255, blank=True, null=True)
    og_description_en = models.TextField(blank=True, null=True)
    og_description_np = models.TextField(blank=True, null=True)
    og_image = models.ImageField(upload_to='seo/seometadata/', null=True, blank=True)

    canonical_url = models.URLField(blank=True, null=True)
    robots = models.CharField(max_length=50, default="index,follow")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "seo_metadata"
        unique_together = ("content_type", "object_id")
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def __str__(self):
        return f"SEO - {self.content_type} #{self.object_id}"
