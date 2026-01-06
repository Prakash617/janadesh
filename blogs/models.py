from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
import uuid

class BlogCategory(models.Model):
    """Blog categories"""
    name_en = models.CharField(max_length=100)
    name_np = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True)
    description_en = models.TextField(blank=True, null=True)
    description_np = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'blog_categories'
        verbose_name_plural = 'Blog Categories'

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
    content_en = models.TextField()
    content_np = models.TextField(blank=True, null=True)
    excerpt_en = models.TextField(blank=True, null=True)
    excerpt_np = models.TextField(blank=True, null=True)
    featured_image = models.ImageField(upload_to='blogs/blog/', null=True, blank=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, related_name='blogs')
    tags = models.ManyToManyField(BlogTag, blank=True, related_name='blogs')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    view_count = models.IntegerField(default=0)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'blogs'
        ordering = ['-published_at', '-created_at']

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
    content = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'comments'
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.blogs.title_en if self.blogs else 'Unknown'}"
    
    
    
# class User(AbstractUser):
#     """Extended User model with additional fields"""
#     PROVINCE_CHOICES = [
#         ('koshi', 'Koshi'),
#         ('gandaki', 'Gandaki'),
#         ('madhesh', 'Madhesh'),
#         ('bagmati', 'Bagmati'),
#         ('lumbini', 'Lumbini'),
#         ('sudurpashchim', 'Sudurpashchim'),
#         ('karnali', 'Karnali'),
#     ]
    
#     ROLE_CHOICES = [
#         ('admin', 'Admin'),
#         ('member', 'Member'),
#         ('volunteer', 'Volunteer'),
#         ('donor', 'Donor'),
#     ]
    
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     phone_number = models.CharField(max_length=15, blank=True, null=True)
#     province = models.CharField(max_length=20, choices=PROVINCE_CHOICES, blank=True)
#     role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
#     is_verified = models.BooleanField(default=False)
#     verification_token = models.CharField(max_length=100, blank=True, null=True)
    
#     class Meta:
#         db_table = 'users'
#         verbose_name = 'User'
#         verbose_name_plural = 'Users'
        
#     def __str__(self):
#         return self.username