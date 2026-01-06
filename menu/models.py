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

    def __str__(self):
        return f"{self.name} ({self.location})"


class MenuItem(models.Model):
    """Menu items with multi-level support"""
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='items')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    label_en = models.CharField(max_length=100)
    label_np = models.CharField(max_length=100, blank=True, null=True)
    url = models.CharField(max_length=255)
    order = models.IntegerField(default=0)
    icon = models.CharField(max_length=50, blank=True, null=True)
    is_external = models.BooleanField(default=False) #for external links
    open_new_tab = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'menu_items'
        ordering = ['order']

    def __str__(self):
        return self.label_en
