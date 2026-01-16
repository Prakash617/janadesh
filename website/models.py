from django.db import models



class About(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "about"
        ordering = ["-created_at"]

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

    def __str__(self):
        return f"Image for {self.about.title}"
    
    
class FutureVision(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True)
    description = models.TextField()

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

    def __str__(self):
        return self.title
    
class SocialMediaLink(models.Model):
    PLATFORM_CHOICES = [
        ("facebook", "Facebook"),
        ("instagram", "Instagram"),
        ("twitter", "Twitter / X"),
        ("youtube", "YouTube"),
        ("linkedin", "LinkedIn"),
        ("tiktok", "TikTok"),
        # ("website", "Website"),
    ]

    platform = models.CharField(
        max_length=50,
        choices=PLATFORM_CHOICES
    )
    url = models.URLField()
    icon = models.CharField(
        max_length=100,
        blank=True,
        help_text="FontAwesome or icon class (e.g. fa-facebook)"
    )

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "social_media_links"
        ordering = ["order"]

    def __str__(self):
        return self.get_platform_display()

