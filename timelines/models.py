from django.db import models

# Create your models here.
class Timeline(models.Model):
    """Timeline for career/organizational history"""
    year = models.IntegerField()
    month = models.IntegerField(blank=True, null=True, help_text="Month (1-12)")
    title_en = models.CharField(max_length=255)
    title_np = models.CharField(max_length=255, blank=True, null=True)
    description_en = models.TextField()
    description_np = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='timelines/timeline/', null=True, blank=True)
    is_milestone = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'timeline'
        ordering = ['-year', '-month', 'order']

    def __str__(self):
        return f"{self.year} - {self.title_en}"