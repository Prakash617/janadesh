from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings


class Page(models.Model):
    """Model for creating dynamic pages in Django"""
    
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    )
    
    # Basic Information
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    
    # Content
    meta_description = models.CharField(
        max_length=160, blank=True, help_text="SEO meta description"
    )
    content = models.TextField(help_text="Main page content (HTML allowed)")
    excerpt = models.TextField(
        blank=True, max_length=300, help_text="Short summary of the page"
    )
    
    featured_image = models.ImageField(upload_to='pages/', blank=True, null=True)
    
    # SEO
    seo_title = models.CharField(
        max_length=70, blank=True, help_text="Custom title for search engines"
    )
    keywords = models.CharField(
        max_length=255, blank=True, help_text="Comma-separated keywords"
    )
    
    # Author and Timestamps
    # author = models.ForeignKey(User, on_delete=models.SET_NULL, 
    #                           null=True, related_name='pages')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Auto-generate slug from title if not provided
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Set SEO title to title if not provided
        if not self.seo_title:
            self.seo_title = self.title
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        """Return the URL for this page"""
        return reverse('page-detail', kwargs={'slug': self.slug})
    
    def get_full_url(self):
        return f"{settings.SITE_URL}{self.get_absolute_url()}"
    
    @property
    def is_published(self):
        """Check if page is published"""
        return self.status == 'published'
