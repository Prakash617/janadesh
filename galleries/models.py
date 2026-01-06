from django.db import models

# Create your models here.
class Gallery(models.Model):
    """Gallery albums"""
    title_en = models.CharField(max_length=255)
    title_np = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True)
    description_en = models.TextField(blank=True, null=True)
    description_np = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='galleries/covers/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'galleries'
        ordering = ['order', '-created_at']
        verbose_name_plural = 'Galleries'

    def __str__(self):
        return self.title_en


class GalleryImage(models.Model):
    """Images within gallery albums"""
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='galleries/images/', blank=True, null=True)
    caption_en = models.TextField(blank=True, null=True)
    caption_np = models.TextField(blank=True, null=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'gallery_images'
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.gallery.title_en} - Image {self.order}"