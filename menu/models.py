from django.db import models

class Menu(models.Model):
    """Menu management"""
    MENU_LOCATION_CHOICES = [
        ('header', 'Header'),
        ('footer', 'Footer'),
        ('sidebar', 'Sidebar'),
    ]
    
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=20, choices=MENU_LOCATION_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'menus'
        verbose_name = 'Menu'
        verbose_name_plural = 'Menu'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.location})"


class MenuItem(models.Model):
    """Menu items with multi-level support"""
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='items')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    label_en = models.CharField(max_length=100)
    label_np = models.CharField(max_length=100, blank=True, null=True)
    page = models.ForeignKey(
        'page.page',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Select a page OR enter a custom URL"
    )
    url = models.CharField(max_length=255,help_text="Auto fill page url OR enter a custom URL", blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    sub_title = models.CharField(max_length=255, blank=True, null=True)
    order = models.IntegerField(default=0)
    icon = models.CharField(max_length=50, blank=True, null=True)
    is_external = models.BooleanField(
        default=False, 
        help_text="Check if this item is an external link"
    ) #for external links
    open_new_tab = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'menu_items'
        ordering = ['order']
        verbose_name = 'Menu Item'
        verbose_name_plural = 'Menu Item'
        
    def save(self, *args, **kwargs):
        # Auto-fill URL from Page
        if self.page:
            self.url = self.page.get_full_url()
            self.is_external = False
        super().save(*args, **kwargs)

    def __str__(self):
        return self.label_en
