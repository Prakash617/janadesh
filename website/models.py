from django.db import models
from tinymce.models import HTMLField

class HeroSection(models.Model):
    # English
    title_en = models.CharField(max_length=255)
    title_np = models.CharField(max_length=255)
    subtitle_en = models.CharField(max_length=255, blank=True)
    subtitle_np = models.CharField(max_length=255, blank=True)
    description_en = HTMLField(blank=True, null=True)
    description_np = HTMLField(blank=True, null=True)
    button_text_en = models.CharField(max_length=255, blank=True)
    button_text_np = models.CharField(max_length=255, blank=True)

    # Nepali

    # Common
    button_url = models.URLField(blank=True)
    main_image = models.ImageField(upload_to="hero_section/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title_en

    class Meta:
        db_table = "hero_section"
        ordering = ["-created_at"]
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Section"
        
class HeroNews(models.Model):
    hero_section = models.ForeignKey(
        HeroSection,
        on_delete=models.CASCADE,
        related_name="hero_news",
        null=True
    )
    # English
    description_en = HTMLField(blank=True, null=True)

    # Nepali
    description_np = HTMLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (self.description_en or "")[:50]

    class Meta:
        db_table = "hero_news"
        ordering = ["-created_at"]
        verbose_name = "Hero News"
        verbose_name_plural = "Hero News"



class About(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True)
    description = HTMLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "about"
        ordering = ["-created_at"]
        verbose_name = "About"
        verbose_name_plural = "About"

    def __str__(self):
        return self.title

class AboutImage(models.Model):
    about = models.ForeignKey(
        About,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="about/")
    caption = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "about_images"
        verbose_name = "About Image"
        verbose_name_plural = "About Image"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Image for {self.about.title}"
    
    
class FutureVision(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True)
    description = HTMLField(blank=True, null=True)

    image = models.ImageField(
        upload_to="future_vision/",
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "future_vision"
        ordering = ["-created_at"]
        verbose_name = "Future Vision"
        verbose_name_plural = "Future Vision"

    def __str__(self):
        return self.title
    
    
    
class SocialPlatform(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    icon = models.CharField(
        max_length=100,
        help_text="FontAwesome / icon class (e.g. fa-brands fa-facebook)"
    )

    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "social_platforms"
        ordering = ["order"]
        verbose_name = "Social Platform Icon"
        verbose_name_plural = "Social Platform Icon"

    def __str__(self):
        return self.name

class SocialMediaLink(models.Model):
    platform = models.OneToOneField(
        SocialPlatform,
        on_delete=models.CASCADE,
        related_name="link",null=True
        
    )

    url = models.URLField()

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "social_media_links"
        ordering = ["order"]
        verbose_name = "Social Platform"
        verbose_name_plural = "Social Platform"

    def __str__(self):
        return self.platform.name
