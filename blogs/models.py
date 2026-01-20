from django.db import models
from django.utils.text import slugify
from django.conf import settings
import uuid
from tinymce.models import HTMLField
from django.contrib.auth import get_user_model

User = get_user_model()

class BlogCategory(models.Model):
    """Blog categories"""
    name_en = models.CharField(max_length=100)
    name_np = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True)
    description_en = HTMLField(blank=True, null=True)
    description_np = HTMLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'blog_categories'
        verbose_name = 'Blog Category'
        verbose_name_plural = 'Blog Category'
        
    def __str__(self):
        return self.name_en
    
    
class BlogTag(models.Model):
    """Blog tags"""
    name_en = models.CharField(max_length=50)
    name_np = models.CharField(max_length=50, blank=True, null=True)
    slug = models.SlugField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'blog_tags'
        verbose_name = 'Blog Tag'
        verbose_name_plural = 'Blog Tag'

    def __str__(self):
        return self.name_en


class Blog(models.Model):
    """Blog/News articles"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    title_en = models.CharField(max_length=255)
    title_np = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True)
    content_en = HTMLField()
    content_np = HTMLField(blank=True, null=True)
    excerpt_en = HTMLField(blank=True, null=True)
    excerpt_np = HTMLField(blank=True, null=True)
    featured_image = models.ImageField(upload_to='blogs/blog/', null=True, blank=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.PROTECT, related_name='blogs')
    tags = models.ManyToManyField(BlogTag, blank=True, related_name='blogs')
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='blogs')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,null=True, default='draft')
    is_featured = models.BooleanField(default=False)
    view_count = models.IntegerField(default=0)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'blogs'
        ordering = ['-published_at', '-created_at']
        verbose_name = 'Blog'
        verbose_name_plural = 'Blog'

    def __str__(self):
        return self.title_en

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title_en)
        super().save(*args, **kwargs)


class Comment(models.Model):
    """Comments on news articles"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('hidden', 'Hidden'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    blogs = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True, blank=True, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    content = HTMLField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'comments'
        verbose_name = 'Comment'
        verbose_name_plural = 'Comment'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.blogs.title_en if self.blogs else 'Unknown'}"