from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from website.models import About, AboutImage,FutureVision,SocialMediaLink,SocialPlatform,HeroNews,HeroSection

class AboutImageInline(admin.TabularInline):
    model = AboutImage
    extra = 1


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "action_buttons")
    inlines = [AboutImageInline]

    def action_buttons(self, obj):
        edit_url = reverse('admin:website_about_change', args=[obj.id])
        return format_html(
            '<a href="{}" style="padding:4px 10px; background-color:#28A745; color:white; '
            'border-radius:5px; text-decoration:none; margin-right:5px; font-weight:bold;">Edit</a>',
            edit_url
        )
    action_buttons.short_description = 'Actions'


@admin.register(FutureVision)
class FutureVisionAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "created_at", "action_buttons")
    list_filter = ("is_active",)
    search_fields = ("title", "subtitle", "description")
    readonly_fields = ("created_at", "updated_at")
    
    def action_buttons(self, obj):
        edit_url = reverse('admin:website_futurevision_change', args=[obj.id])
        return format_html(
            '<a href="{}" style="padding:4px 10px; background-color:#28A745; color:white; '
            'border-radius:5px; text-decoration:none; margin-right:5px; font-weight:bold;">Edit</a>',
            edit_url
        )
    action_buttons.short_description = 'Actions'
    
@admin.register(SocialPlatform)
class SocialPlatformAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "icon_preview",
        "is_active",
        "order",
        "created_at",
        "action_buttons",
    )

    list_editable = ("is_active", "order")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("order",)

    def icon_preview(self, obj):
        if obj.icon:
            return format_html('<i class="{}"></i>', obj.icon)
        return "-"

    icon_preview.short_description = "Icon"
    
    def action_buttons(self, obj):
        edit_url = reverse('admin:website_socialplatform_change', args=[obj.id])
        return format_html(
            '<a href="{}" style="padding:4px 10px; background-color:#28A745; color:white; '
            'border-radius:5px; text-decoration:none; margin-right:5px; font-weight:bold;">Edit</a>',
            edit_url
        )
    action_buttons.short_description = 'Actions'
    
@admin.register(SocialMediaLink)
class SocialMediaLinkAdmin(admin.ModelAdmin):
    list_display = (
        "platform",
        "platform_icon",
        "url",
        "order",
        "is_active",
        "action_buttons",
    )

    list_filter = ("platform", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("platform__name", "url")
    ordering = ("order",)

    def platform_icon(self, obj):
        return obj.platform.icon

    platform_icon.short_description = "Icon"


    def action_buttons(self, obj):
        edit_url = reverse('admin:website_socialmedialink_change', args=[obj.id])
        return format_html(
            '<a href="{}" style="padding:4px 10px; background-color:#28A745; color:white; '
            'border-radius:5px; text-decoration:none; margin-right:5px; font-weight:bold;">Edit</a>',
            edit_url
        )
    action_buttons.short_description = 'Actions'
from django.contrib import admin
from .models import HeroSection, HeroNews


class HeroNewsInline(admin.StackedInline):
    model = HeroNews
    extra = 0
    fields = ("description_en", "description_np")
    show_change_link = True


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ("title_en", "title_np", "created_at")
    inlines = [HeroNewsInline]

    fieldsets = (
        ("Content", {
            "fields": (
                "title_en",
                "subtitle_en",
                "description_en",
                "button_text_en",
                "title_np",
                "subtitle_np",
                "description_np",
                "button_text_np",
            )
        }),
        ("Media & Action", {
            "fields": (
                "button_url",
                "main_image",
            )
        }),
        
    )

    readonly_fields = ("created_at", "updated_at")

    def has_add_permission(self, request):
        # Allow add only if no HeroSection exists (singleton)
        return not HeroSection.objects.exists()
