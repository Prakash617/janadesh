from django.contrib import admin
from .models import Organization, Leadership, MembershipRegistration, Policy, Donation

# Register your models here.

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'slug', 'email', 'phone', 'website', 'created_at')
    search_fields = ('name_en', 'name_np', 'description_en', 'description_np')
    prepopulated_fields = {'slug': ('name_en',)}
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('name_en', 'name_np', 'slug', 'logo', 'banner', 'description_en', 'description_np')
        }),
        ('Details', {
            'fields': ('established_date', 'manifesto_en', 'manifesto_np', 'manifesto_document')
        }),
        ('Contact', {
            'fields': ('email', 'phone', 'address_en', 'address_np', 'website')
        }),
        ('Social Media', {
            'fields': ('facebook', 'twitter', 'instagram', 'youtube')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

admin.site.register(Organization, OrganizationAdmin)

class LeadershipAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'position_en', 'member_type', 'is_featured', 'is_active', 'order')
    list_filter = ('member_type', 'is_featured', 'is_active')
    search_fields = ('name_en', 'name_np', 'position_en', 'position_np', 'bio_en', 'bio_np')
    prepopulated_fields = {'slug': ('name_en',)}
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Leadership, LeadershipAdmin)

class MembershipRegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'membership_type', 'province', 'status', 'created_at', 'approved_by')
    list_filter = ('membership_type', 'province', 'status')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'address', 'citizenship_number', 'occupation')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'

admin.site.register(MembershipRegistration, MembershipRegistrationAdmin)

class PolicyAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_featured', 'order', 'created_at')
    list_filter = ('category', 'is_featured')
    search_fields = ('title', 'title_ne', 'description', 'description_ne', 'content', 'content_ne')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Policy, PolicyAdmin)

class DonationAdmin(admin.ModelAdmin):
    list_display = ('donor_name', 'amount', 'currency', 'payment_method', 'status', 'is_anonymous', 'created_at')
    list_filter = ('payment_method', 'status', 'currency', 'is_anonymous')
    search_fields = ('donor_name', 'donor_email', 'transaction_id')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'

admin.site.register(Donation, DonationAdmin)
