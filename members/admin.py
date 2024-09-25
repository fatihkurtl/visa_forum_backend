from django.contrib import admin
from django.utils.html import format_html
from .models import Member, MemberRole, Token

class MemberRoleInline(admin.StackedInline):
    model = MemberRole
    extra = 0

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = (
        'firstname', 'lastname', 'username', 'email',
        'is_active', 'email_verified', 'created_at', 'updated_at', 'profile_image_preview'
    )
    search_fields = ('firstname', 'lastname', 'username', 'email')
    list_filter = ('is_active', 'email_verified', 'memberrole__role')
    inlines = [MemberRoleInline]

    fieldsets = (
        (None, {
            'fields': ('firstname', 'lastname', 'username', 'email', 'profile_image', 'password', 'bio', 'expertise', 'email_notifications', 'is_active', 'terms', 'ip_address')  # country_of_interest eklendi
        }),
        ('Permissions', {
            'fields': ('email_verified',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    readonly_fields = ('created_at', 'updated_at', 'ip_address')

    def profile_image_preview(self, obj):
        """Profile image preview for admin panel."""
        if obj.profile_image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 50%;" />', obj.profile_image.url)
        return "Profil resmi yok"
    
    profile_image_preview.short_description = 'Profil resmi'

@admin.register(MemberRole)
class MemberRoleAdmin(admin.ModelAdmin):
    list_display = ('member', 'role', 'created_at')
    search_fields = ('member__username', 'role')

@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('member', 'token', 'created_at', 'expires_at')
    search_fields = ('member__username', 'token')
    list_filter = ('created_at', 'expires_at')

    fieldsets = (
        (None, {
            'fields': ('member', 'token', 'created_at', 'expires_at')
        }),
    )

    readonly_fields = ('created_at',)