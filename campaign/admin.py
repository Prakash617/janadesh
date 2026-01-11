from django.contrib import admin
from .models import Campaign, CampaignActivity, Volunteer

# Register your models here.
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'start_date', 'end_date', 'status', 'is_featured', 'created_at')
    list_filter = ('status', 'is_featured', 'start_date', 'end_date')
    search_fields = ('title_en', 'title_np', 'description_en', 'description_np')
    prepopulated_fields = {'slug': ('title_en',)}
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title_en', 'title_np', 'slug', 'banner', 'description_en', 'description_np', 'goal')
        }),
        ('Schedule & Location', {
            'fields': ('start_date', 'end_date', 'region_en', 'region_np')
        }),
        ('Status', {
            'fields': ('status', 'is_featured', 'created_by')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

admin.site.register(Campaign, CampaignAdmin)

class CampaignActivityAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'campaign', 'activity_type', 'date', 'location_en', 'participants_count', 'created_at')
    list_filter = ('activity_type', 'campaign', 'date')
    search_fields = ('title_en', 'title_np', 'description_en', 'description_np', 'location_en', 'location_np')
    date_hierarchy = 'date'
    exclude = ('created_at', 'updated_at')
    

admin.site.register(CampaignActivity, CampaignActivityAdmin)

class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'campaign', 'is_active', 'created_at')
    list_filter = ('is_active', 'campaign')
    search_fields = ('name', 'email', 'phone', 'address', 'skills')
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Volunteer, VolunteerAdmin)
