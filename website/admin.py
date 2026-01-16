from django.contrib import admin
from .models import About, AboutImage


class AboutImageInline(admin.TabularInline):
    model = AboutImage
    extra = 1


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    inlines = [AboutImageInline]
