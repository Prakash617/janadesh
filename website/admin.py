from django.contrib import admin
from website.models import About, AboutImage,FutureVision,SocialMediaLink

class AboutImageInline(admin.TabularInline):
    model = AboutImage
    extra = 1


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    inlines = [AboutImageInline]


@admin.register(FutureVision)
class FutureVisionAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("title", "subtitle", "description")
    readonly_fields = ("created_at", "updated_at")
    
@admin.register(SocialMediaLink)
class SocialMediaLinkAdmin(admin.ModelAdmin):
    list_display = ("platform", "url", "order","icon", "is_active")
    list_filter = ("platform", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("platform", "url")