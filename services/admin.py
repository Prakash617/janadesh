from django.contrib import admin
from .models import Service

# Register your models here.
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'slug', 'is_active', 'order', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title_en', 'title_np', 'description_en', 'description_np')
    prepopulated_fields = {'slug': ('title_en',)}
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title_en', 'title_np', 'slug', 'icon', 'image', 'description_en', 'description_np')
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

admin.site.register(Service, ServiceAdmin)
