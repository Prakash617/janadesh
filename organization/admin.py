from django.contrib import admin
from .models import Organization, Leadership, MembershipRegistration, Policy, Donation
# ,PolicyCategory
from django.utils.html import format_html


# Register your models here.
# @admin.register(PolicyCategory)
# class PolicyCategoryAdmin(admin.ModelAdmin):
#     list_display = (
#         "name_en",
#         "name_ne",
#         "slug",
#         "order",
#         "is_active",
#         "created_at",
#     )

#     list_filter = ("is_active",)
#     list_editable = ("is_active","order")
#     search_fields = ("name_en", "name_ne", "slug")
#     ordering = ("order", "name_en")

#     prepopulated_fields = {"slug": ("name_en",)}

#     fieldsets = (
#         (None, {
#             "fields": ("name_en", "name_ne", "slug", "icon")
#         }),
#         ("Display Settings", {
#             "fields": ("order", "is_active")
#         }),
#         ("Timestamps", {
#             "fields": ("created_at", "updated_at"),
#             "classes": ("collapse",),
#         }),
#     )

#     readonly_fields = ("created_at", "updated_at")

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

@admin.register(MembershipRegistration)
class MembershipRegistrationAdmin(admin.ModelAdmin):
    """Admin interface for MembershipRegistration model"""
    
    list_display = [
        'get_full_name',
        'membership_type',
        'email',
        'province',
        'district',
        'status_badge',
        'created_at'
    ]
    
    list_filter = [
        'status',
        'membership_type',
        'province',
        'gender',
        'created_at',
        'approved_at'
    ]
    
    search_fields = [
        'first_name',
        'last_name',
        'email',
        'phone_number',
        'citizenship_number',
        'district',
        'municipality'
    ]
    
    readonly_fields = [
        'id',
        'created_at',
        'updated_at',
        'approved_at',
        'get_full_address'
    ]
    
    fieldsets = (
        ('Membership Information', {
            'fields': ('membership_type', 'status')
        }),
        ('Personal Information', {
            'fields': (
                'first_name',
                'last_name',
                'father_name',
                'date_of_birth',
                'gender',
                'phone_number',
                'email',
            )
        }),
        ('Location Details', {
            'fields': (
                'province',
                'district',
                'municipality',
                'ward_number',
                'village_settlement',
                'address',
                'get_full_address',
            )
        }),
        ('Documents', {
            'fields': (
                'citizenship_number',
                'passport_photo',
                'citizenship_copy',
            )
        }),
        ('Additional Information', {
            'fields': (
                'occupation',
                'motivation',
                # 'terms_accepted',
            )
        }),
        ('Approval Information', {
            'fields': (
                'approved_by',
                'approved_at',
                'rejection_reason',
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    actions = ['approve_applications', 'reject_applications']
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Full Name'
    
    def status_badge(self, obj):
        colors = {
            'pending': '#ffc107',
            'approved': '#28a745',
            'rejected': '#dc3545'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def approve_applications(self, request, queryset):
        count = 0
        for membership in queryset.filter(status='pending'):
            membership.approve(request.user)
            count += 1
        self.message_user(request, f'{count} application(s) approved successfully.')
    approve_applications.short_description = 'Approve selected applications'
    
    def reject_applications(self, request, queryset):
        count = queryset.filter(status='pending').update(
            status='rejected',
            rejection_reason='Rejected by admin'
        )
        self.message_user(request, f'{count} application(s) rejected.')
    reject_applications.short_description = 'Reject selected applications'


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
