from django.contrib import admin
from .models import Timeline

# Register your models here.
class TimelineAdmin(admin.ModelAdmin):
    list_display = ('year', 'month', 'title_en', 'is_milestone', 'order', 'created_at')
    list_filter = ('year', 'is_milestone')
    search_fields = ('title_en', 'title_np', 'description_en', 'description_np')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('year', 'month', 'title_en', 'title_np', 'description_en', 'description_np', 'image')
        }),
        ('Settings', {
            'fields': ('is_milestone', 'order')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

admin.site.register(Timeline, TimelineAdmin)
